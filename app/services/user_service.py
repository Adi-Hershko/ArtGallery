import bcrypt
from app.dals.user_dal import add_user, find_user
from app.exceptions import UserNotFoundException, PasswordNotMatchException, OperationError, UserAlreadyExist
from ..pydantic_models.user_models.user_request_model import UserBaseRequestModel, UserInternalRequestModel, UserSearchRequestModel
from ..pydantic_models.user_models.user_response_model import UserBaseResponseModel, UserInternalResponseModel

async def create_user(user: UserBaseRequestModel) -> None:
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)    
        await add_user(UserInternalRequestModel(username=user.username, password=hashed_password))
    except UserAlreadyExist:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise OperationError("Error creating user.")

async def validate_user(user: UserBaseRequestModel) -> UserBaseResponseModel:
    fetched_user = await find_user(UserSearchRequestModel(username=user.username))
    if fetched_user is None:
        raise UserNotFoundException("User not found.")

    if not bcrypt.checkpw(user.password.encode("utf-8"), fetched_user.password):
        raise PasswordNotMatchException("Password does not match.")
        
    return UserBaseResponseModel(username=fetched_user.username, is_active=True)