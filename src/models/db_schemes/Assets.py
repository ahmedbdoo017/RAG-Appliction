from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Assets(BaseModel):

    id: Optional[ObjectId] = Field(None , alias='_id')
    assets_project_id : ObjectId
    assets_type : str =Field(..., min_length=1)
    assets_name : str =Field(..., min_length=1)
    assets_size : int =Field(ge=0 , default=None)
    assets_pushed_at : datetime =Field(default=datetime.utcnow)
    asset_config : dict =Field(default=None)# may be use later

    @classmethod
    def get_indexes(cls):
        # used for search using asset_project_id only or use asset_project_id only and asset name both 
        return[
            {
                "key" : [
                    ("assets_project_id", 1)
                ],
                "name": "assets_project_id_index_1",
                "unique":False 
            },
            {
                "key" : [
                    ("assets_project_id", 1),
                     ("assets_name", 1)
                    
                ],
                "name": "assets_project_id_name_index_1",
                "unique":True
            }
        ]


    # Allow ObjectId type
    model_config = {"arbitrary_types_allowed": True}


