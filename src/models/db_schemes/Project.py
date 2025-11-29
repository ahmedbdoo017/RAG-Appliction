from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    # MongoDB automatically generates _id, so it's optional when creating a project
    id: Optional[ObjectId] = Field(None , alias='_id')

    # Required field: project_id must be provided and must have at least 1 character
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id (cls , value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        
        return value
    
    @classmethod
    def get_indexes(cls):

        return[
            {
                "key" : [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique":True
            }
        ]

    model_config = {"arbitrary_types_allowed": True}
