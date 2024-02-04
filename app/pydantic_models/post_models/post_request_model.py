from pydantic import BaseModel, Field, constr
from uuid import UUID
from typing import Optional

# Field(...) means that the field is required
class PostUploadRequestModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[constr(min_length=3, max_length=200)] = Field(
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    pathToImage: str = Field(..., min_length=3, max_length=300)

    # An example of how to use this model
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "title": "My new post",
                "description": "This is a new post",
                "pathToImage": "https://www.example.com/image.jpg"
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


class PostUpdateRequestModel(BaseModel):
    postId: UUID = Field(..., description="The id of the post")
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[constr(min_length=3, max_length=200)] = Field(
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    pathToImage: Optional[str] = Field(None, min_length=3, max_length=300)

    # An example of how to use this model
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My new post",
                "description": "This is a new post",
                "pathToImage": "https://www.example.com/image.jpg"
            }
        }