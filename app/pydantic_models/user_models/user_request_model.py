from pydantic import BaseModel, Field

class UserBaseRequestModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    # An example of how to use this model
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }

class UserInternalRequestModel(BaseModel):
    username: str
    password: bytes # This is the hashed password

class UserSearchRequestModel(BaseModel):
    username: str