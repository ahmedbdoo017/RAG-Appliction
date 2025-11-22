from .BaseDataModel import BaseDataModel
from .db_schemes import Assets
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)

        # get connection with projects table from monogo database
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    
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

        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Assets.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name =index["name"],
                    unique = index["unique"]
                )
    
    async def create_asset(self, asset:Assets):
        result = await self.collection.insert_one(asset.dict(by_alias=True ,exclude_unset=True))
        asset.id = result.inserted_id
        return asset
    
    async def get_all_project_aseets(self, asset_project_id:str ,aseet_type:str):

        records = await self.collection.find({
            "assets_project_id": ObjectId(asset_project_id), 
            "assets_type" : aseet_type
            }).to_list(length=None)
        
        return [
            Assets(**record)
            for record in records
        ]
    
    async def get_aseet_record(self, asset_project_id:str ,aseet_name:str):

        record = await self.collection.find_one({
             "asset_project_id": ObjectId(asset_project_id), 
             "aseet_name" : aseet_name
        })

        if record :
            return Assets(**record)
        
        else:
            return None


    

    
 