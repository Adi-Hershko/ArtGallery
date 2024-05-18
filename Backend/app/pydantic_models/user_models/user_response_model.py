from pydantic import BaseModel

class UserBaseResponseModel(BaseModel):
    username: str
    is_active: bool

    # An example of how to use this model, for documentation purposes
    class Config:
        # orm_mode = True tells Pydantic to read the data even if it is not a dict
        orm_mode = True
        # schema_extra is used to add an example of how to use this model, password is not included for security reasons
        schema_extra = {
            "example": {
                "username": "johndoe",
                "is_active": True
            }
        }

class UserInternalResponseModel(BaseModel):
    username: str
    password: bytes # This is the hashed password

    # An example of how to use this model, for documentation purposes
    class Config:
        # orm_mode = True tells Pydantic to read the data even if it is not a dict
        orm_mode = True
        # schema_extra is used to add an example of how to use this model, password is not included for security reasons
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "hashedpassword"
            }
        }
