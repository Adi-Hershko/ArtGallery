from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field, constr
from uuid import UUID
from typing import Optional


# Field(...) means that the field is required
class PostUploadRequestModel(BaseModel):
    username: str = Form(..., min_length=3, max_length=50)
    title: str = Form(..., min_length=3, max_length=50)
    description: Optional[constr(min_length=3, max_length=200)] = Form( # type: ignore
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    Image: UploadFile = File(..., description="The image of the post")

    # An example of how to use this model
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

    # An example of how to use this model
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

    # An example of how to use this model
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
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[constr(min_length=3, max_length=200)] = Field( # type: ignore
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    path_to_image: Optional[str] = Field(None, min_length=3, max_length=300)

    # An example of how to use this model
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My new post",
                "description": "This is a new post",
                "path_to_image": "https://www.example.com/image.jpg"
            }
        }

    def convert_to_dict(self):
        return {
            "postId": self.postId,
            "title": self.title,
            "description": self.description,
            "path_to_image": self.path_to_image,
        }
