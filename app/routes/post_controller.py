from fastapi import APIRouter
from typing import Optional
from app.services.post_service import get_feed, create_post

post_controller_router = APIRouter()


@post_controller_router.get("/posts", tags=["Posts"])
async def get_posts(username: Optional[str] = None, title: Optional[str] = None):
    return await get_feed({"username": username, "title": title})


@post_controller_router.post("/upload-post", tags=["Posts"])
async def upload_post(username: str, title: str, description: str, pathToImage: str):
    await create_post(username, title, description, pathToImage)
    return {"message": f"{title} has been uploaded."}


#TODO: Add a route to delete a post
#TODO: Add a route to update a post