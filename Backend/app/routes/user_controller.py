from fastapi import APIRouter
from kink import inject

from app.services.user_service import UserService
from app.routes.middlewares.auth_middleware import AccessTokenCreator
from app.pydantic_models.user_models.user_request_model import UserBaseRequestModel
from app.pydantic_models.user_models.user_response_model import UserBaseResponseModel


@inject
class UserController:
    def __init__(self, user_service: UserService, access_token_creator: AccessTokenCreator):
        self.router = APIRouter()
        self.user_service = user_service
        self.access_token_creator = access_token_creator
        self.register_routes()

    def register_routes(self):
        self.router.get("/", tags=["Root"])(self.root)
        self.router.post("/sign-up", tags=["Users"])(self.sign_up)
        self.router.post("/sign-in", tags=["Users"])(self.sign_in)

    async def root(self) -> dict:
        return {"message": "Welcome to Art Gallery!"}

    async def sign_up(self, user: UserBaseRequestModel) -> dict:
        await self.user_service.create_user(user)
        access_key = self.access_token_creator.create_access_token(username=user.username)
        return {"message": f"{user.username} has been signed up.", "username": user.username, "access_key": access_key}

    async def sign_in(self, user: UserBaseRequestModel) -> UserBaseResponseModel:
        user_response = await self.user_service.validate_user(user)
        if user_response is not None:
            user_response.access_key = self.access_token_creator.create_access_token(username=user_response.username)

        return user_response

    