import bcrypt
from app.dals.user_dal import create_user, get_hashed_password
from ..DB.db_operations import DatabaseOperations

async def create_user(username:str, password:str) -> bool:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    db = DatabaseOperations()
    db.add_user(username, hashed_password)
    return True
    
async def validate_user(username: str, password: str):
    hashed_password = get_hashed_password(username, password)
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)