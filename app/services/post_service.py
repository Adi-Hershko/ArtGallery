from app.dals.post_dal import add_post, get_all_posts
from app.dals.user_dal import find_user
from app.exceptions import UserNotFoundException

async def get_feed(filters: dict = dict()):
    filtered_dict = {parameter: condition for parameter, condition in filters.items() if condition is not None}
    feed = await get_all_posts(filtered_dict)
    return feed

async def create_post(username: str, title: str, description: str, pathToImage: str):
    user = await find_user(username)
    if user is None:
        raise UserNotFoundException("User not found.")
    await add_post(username, title, description, pathToImage)    

