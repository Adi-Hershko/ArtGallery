from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime
from uuid import UUID


class PostGetResponseModel(BaseModel):
    postId: UUID = Field(..., description="The id of the post")
    username: str = Field(..., min_length=3, max_length=50)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[constr(min_length=3, max_length=200)] = Field( # type: ignore
        default=None, 
        description="The description of the post",
        example="This is an example description of a post."
    )
    path_to_image: str = Field(..., min_length=3, max_length=300)
    path_to_thumbnail: str = Field(..., min_length=3, max_length=300)
    insertionTime: datetime = Field(..., description="The time the post was inserted.")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "postId": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "title": "My new post",
                "description": "This is a new post",
                "path_to_image": "https://www.example.com/image.jpg",
                "insertionTime": "2023-01-01T12:00:00"
            }
        }
