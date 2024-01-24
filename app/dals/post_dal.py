from app.exceptions import UserNotFoundException
from app.exceptions import PostNotFoundException
from ..DB.models import User, Post

async def add_post()