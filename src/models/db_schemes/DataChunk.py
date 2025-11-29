from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class DataChunk (BaseModel):
    # MongoDB automatically generates _id, so it's optional when creating a project
    id: Optional[ObjectId] = Field(None , alias='_id')
    chunk_txt : str = Field(... ,min_length=1)
    chunk_metadata : dict
    chunk_order : int = Field(...,gt =0)
    chunk_project_id : ObjectId # used to link with project id in project schema (foregin_key)
    chunk_asset_id : ObjectId 
    @classmethod
    def get_indexes(cls):

        return[
            {
                "key" : [
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "unique":False # false because we may be have more than one chunk belong to the same chunk project_id
            }
        ]


    # Allow ObjectId type
    model_config = {"arbitrary_types_allowed": True}

class RetrivedDocument(BaseModel):
    text:str
    score:float


