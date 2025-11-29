from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel (BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client)

        # get connection with projects table from monogo database
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    
    @classmethod
    async def create_instance(cls, db_client):
        # when you need to call asynic function when initalization
        # note that you take the paramter that __init__ take to pass for it 
        # note that when you creat an object from this class you will use this static function rather than __init_

        instance= cls(db_client) # to pass paramter to class __init__
        await instance.init_collection()
        return instance

    
    async def init_collection(self):
        all_collection = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            indexes = DataChunk.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name =index["name"],
                    unique = index["unique"]
                )
 

    async def create_chunk(self, chunk :DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True ,exclude_unset=True))
        chunk_id = result.inserted_id
        return chunk
    
    async def get_chunk (self, chunk_id :str):
        result = await self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })

        if result is None :
            return None
        
        return DataChunk(**result)
    
    async def insert_many_chunks (self, chunks: list , batch_size : int=100):

        for i in range (0, len(chunks), batch_size):
            batch = chunks[i :i+batch_size]

            operations = [
                InsertOne(chunk.dict(by_alias=True ,exclude_unset=True))
                for chunk in batch
            ]
            
            await self.collection.bulk_write(operations)

        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id :ObjectId):
        result =await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count
    
    async def get_project_chunks (self, project_id: ObjectId, page_no: int=1, page_size: int=50):

        results = await self.collection.find({
            "chunk_project_id": project_id
            }).skip((page_no-1) * page_size).limit(page_size).to_list(length=None)
        
        return [
            DataChunk(**record)
            for record in results
        ]
    


