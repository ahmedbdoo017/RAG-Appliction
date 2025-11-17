from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)

        # get connection with projects table from monogo database
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    
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

        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()

            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name =index["name"],
                    unique = index["unique"]
                )
 

    async def create_project (self, project : Project):

        result = await self.collection.insert_one(project.dict(by_alias=True ,exclude_unset=True)) # convert project object into dictionry as mongodb accept dict only
        project.id = result.inserted_id

        return project # note that now project has an value in it's (_id) paramter that take it from result

    
    async def  get_project_or_create_one (self, project_id:str):
        
        record =await self.collection.find_one({
            "project_id":project_id 
        })
        
        if record is None :
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project
        
        return Project(**record) # convert output dictionary from db to an object to deal with it in code

    
    async def get_all_projects (self, page: int=1 , page_size: int=10):
        # count total number of document 
        total_documents = await self.collection.count_document({})

        # calculate total number of pages
        total_pages = total_documents//page_size
        if total_documents % page_size !=0 :
            total_pages +=1

        cursor = self.collection.find().skip( (page-1) * page_size).limit(page_size)

        projects = []
        async for doc in cursor :
            projects.append(
                Project(**doc)
            )
        
        return projects , total_pages
        

    
    






    
    





