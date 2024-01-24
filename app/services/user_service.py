import bcrypt
from app.dals.user_dal import add_user, find_user
from app.exceptions import UserNotFoundException, PasswordNotMatchException

async def create_user(username:str, password:str) -> bool:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)    
    await add_user(username, hashed_password)
    return True

async def validate_user(username: str, password: str):
    user = await find_user(username)
    if user is None:
        raise UserNotFoundException("User not found.")

    if not bcrypt.checkpw(password.encode("utf-8"), user.password):
        raise PasswordNotMatchException("Password does not match.")

    return True