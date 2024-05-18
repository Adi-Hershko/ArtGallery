from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field, constr
from uuid import UUID
from typing import Optional


# Field(...) means that the field is required
class PostUploadRequestModel(BaseModel):
    username: str = Form(...)
    title: str = Form(...)
    description: Optional[str] = Form( 
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    Image: UploadFile = File(..., description="The image of the post")

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "title": "My new post",
                "description": "This is a new post",
                "Image": "[File.jpg]"
            }
        }


class PostIdSearchRequestModel(BaseModel):
    postId: UUID = Field(..., description="The id of the post")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class PostFeedRequestModel(BaseModel):
    username: Optional[str] = Field(None, description="The username of the user")
    title: Optional[str] = Field(None, description="The title of the post")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "title": "My new post"
            }
        }

    def convert_to_dict(self):
        return {
            "username": self.username,
            "title": self.title
        }


class PostUpdateRequestModel(BaseModel):
    postId: UUID = Field(..., description="The id of the post")
    path_to_image: str = Field(..., description="The path to the image of the post")
    username: str = Field(..., description="The username of the user")
    title: Optional[str] = Field(None)
    description: Optional[str] = Field( 
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    Image: Optional[UploadFile] = File(None, description="The image of the post")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My new post",
                "description": "This is a new post",                
            }
        }

    def create_updates(self):
        updates = {}
        if self.title is not None and self.title.strip() != '':
            updates['title'] = self.title
        if self.description is not None and self.description.strip() != '':
            updates['description'] = self.description        
        return updates
