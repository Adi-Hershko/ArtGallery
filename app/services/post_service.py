from app.dals.post_dal import add_post, get_all_posts, update_post_in_db
from app.dals.user_dal import find_user
from app.exceptions import UserNotFoundException
from uuid import UUID

async def get_feed(filters: dict = dict()):
    filtered_dict = {parameter: condition for parameter, condition in filters.items() if condition is not None}
    return await get_all_posts(filtered_dict)

async def create_post(username: str, title: str, description: str, pathToImage: str):
    user = await find_user(username)
    if user is None:
        raise UserNotFoundException("User not found.")
    await add_post(username, title, description, pathToImage)    

async def filter_updates(postId: UUID, updates: dict):
    filtered_dict = {parameter: condition for parameter, condition in updates.items() if condition is not None}
    if not filtered_dict:
        return
    print("Filtering updates: ", filtered_dict)
    await update_post_in_db(postId, filtered_dict)

