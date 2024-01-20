import bcrypt
from app.dals.user_dal import add_user

async def create_user(username:str, password:str) -> bool:
    salt = bcrypt.gensalt()
    print("Salt: ", salt)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)    
    print("Hashed password: ", hashed_password)
    await add_user(username, hashed_password)
    return True
    
async def validate_user(username: str, password: str):
    pass
    # hashed_password = get_hashed_password(username, password)
    # return bcrypt.checkpw(password.encode("utf-8"), hashed_password)