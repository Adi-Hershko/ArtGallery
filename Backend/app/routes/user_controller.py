from fastapi import APIRouter
from kink import inject

from app.services.user_service import UserService
from ..pydantic_models.user_models.user_request_model import UserBaseRequestModel
from ..pydantic_models.user_models.user_response_model import UserBaseResponseModel


@inject
class UserController:
    def __init__(self, user_service: UserService):
        self.router = APIRouter()
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        self.router.get("/", tags=["Root"])(self.root)
        self.router.post("/sign-up", tags=["Users"])(self.sign_up)
        self.router.post("/sign-in", tags=["Users"])(self.sign_in)

    async def root(self) -> dict:
        return {"message": "Welcome to Art Gallery!"}

    async def sign_up(self, user: UserBaseRequestModel) -> dict:
        await self.user_service.create_user(user)
        return {"message": f"{user.username} has been signed up.", "username": user.username}

    async def sign_in(self, user: UserBaseRequestModel) -> UserBaseResponseModel:
        return await self.user_service.validate_user(user)

    