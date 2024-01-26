from app.dals.post_dal import find_posts_by_title, add_post, find_posts_by_username, get_all_posts
from app.dals.user_dal import find_user
from app.exceptions import PostNotFoundException, FeedNotFoundException, UserNotFoundException

async def get_feed():
    feed = await get_all_posts()
    if not feed:
        raise FeedNotFoundException("Feed not found.")
    return feed

async def create_post(username: str, title: str, description: str, pathToImage: str):
    user = await find_user(username)
    if user is None:
        raise UserNotFoundException("User not found.")
    await add_post(username, title, description, pathToImage)
    return True

async def get_posts_by_username(username: str):
    user = await find_user(username)
    if user is None:
        raise UserNotFoundException("User not found.")
    posts = await find_posts_by_username(username)
    return posts

async def get_posts_by_title(title: str):
    posts = await find_posts_by_title(title)
    return posts