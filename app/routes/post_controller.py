from fastapi import APIRouter, HTTPException
from app.routes.middlewares.auth_middleware import validate_auth
from app.services.post_service import get_feed, create_post, get_posts_by_username, get_posts_by_title

post_controller_router = APIRouter()

#TODO: route of get all posts
@post_controller_router.get("/feed", tags=["Posts"])
async def feed():
    feed = await get_feed()        
    return feed


#TODO: route of get post by username
@post_controller_router.get("/posts-by-user", tags=["Posts"])
async def user_posts(username: str):
    posts = await get_posts_by_username(username)    
    return posts


#TODO: route of get post by title
@post_controller_router.get("/search-posts", tags=["Posts"])
async def search_posts_by_title(title: str):
    posts = await get_posts_by_title(title)
    return posts


#TODO: route of create post
@post_controller_router.post("/upload-post", tags=["Posts"])
async def upload_post(username: str, title: str, description: str, pathToImage: str):
    await create_post(username, title, description, pathToImage)
    return {"message": f"{title} has been uploaded."}

