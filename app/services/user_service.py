import bcrypt
from app.dals.user_dal import add_user, find_user
from app.exceptions import UserNotFoundException, PasswordNotMatchException

async def create_user(username:str, password:str) -> bool:
    salt = bcrypt.gensalt()
    print("Salt: ", salt)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)    
    print("Hashed password: ", hashed_password)
    await add_user(username, hashed_password)
    return True


async def validate_user(username: str, password: str):
    try:
        user = await find_user(username)
        if isinstance(user,UserNotFoundException):            
            return UserNotFoundException(f"User '{username}' not found.")
        print("User: ", user)
        print("Username: ", user.username)        
        if bcrypt.checkpw(password.encode("utf-8"), user.password):
            return True
        else:
            return PasswordNotMatchException(f"Password does not match.")
    except Exception as e:
        print(f"Error inside validate_user: {e}")
        