from fastapi import APIRouter, Depends
from app.services.user_service import create_user, validate_user
from ..pydantic_models.user_models.user_request_model import UserBaseRequestModel
from ..pydantic_models.user_models.user_response_model import UserBaseResponseModel


user_controller_router = APIRouter()

@user_controller_router.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Welcome to Art Gallery!"}


@user_controller_router.post("/sign-up", tags=["Users"])
async def sign_up(user: UserBaseRequestModel = Depends(UserBaseRequestModel)) -> dict:
    await create_user(user)
    return {"message": f"{user.username} has been signed up."}
            

@user_controller_router.post("/sign-in", tags=["Users"])
async def sign_in(user: UserBaseRequestModel = Depends(UserBaseRequestModel)) -> UserBaseResponseModel:
    return await validate_user(user)
    