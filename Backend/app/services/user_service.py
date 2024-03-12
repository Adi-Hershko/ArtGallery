import bcrypt
import inspect
from kink import inject
from app.dals.user_dal import UserDal
from app.exceptions import UserNotFoundException, PasswordNotMatchException, OperationError, UserAlreadyExist
from app.DB.models import User
from app.pydantic_models.user_models.user_request_model import UserBaseRequestModel
from app.pydantic_models.user_models.user_response_model import UserBaseResponseModel
from app import logger


@inject
class UserService:
    def __init__(self, user_dal: UserDal):
        self.user_dal = user_dal

    async def create_user(self, user: UserBaseRequestModel) -> None:
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
            await self.user_dal.add_user(User(username=user.username, password=hashed_password))
        except UserAlreadyExist:
            raise
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            logger.error(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")

    async def validate_user(self, user: UserBaseRequestModel) -> UserBaseResponseModel:
        fetched_user = await self.user_dal.find_user(username=user.username)
        if fetched_user is None:
            raise UserNotFoundException("User not found.")

        if not bcrypt.checkpw(user.password.encode("utf-8"), fetched_user.password):
            raise PasswordNotMatchException("Password does not match.")

        return UserBaseResponseModel(username=fetched_user.username, is_active=True)
