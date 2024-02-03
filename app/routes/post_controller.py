from fastapi import APIRouter
from typing import Optional
from app.services.post_service import get_feed, create_post, filter_updates
from uuid import UUID

post_controller_router = APIRouter()


@post_controller_router.get("/posts", tags=["Posts"])
async def get_posts(username: Optional[str] = None, title: Optional[str] = None):
    return await get_feed({"username": username, "title": title})


@post_controller_router.post("/upload-post", tags=["Posts"])
async def upload_post(username: str, title: str, description: str, pathToImage: str):
    await create_post(username, title, description, pathToImage)
    return {"message": f"{title} has been uploaded."}


@post_controller_router.delete("/delete-post", tags=["Posts"])
async def delete_post(postId: UUID):
    await filter_updates(postId, {"isActive": False})
    return {"message": f"Post {postId} has been deleted."}


@post_controller_router.put("/update-post", tags=["Posts"])
async def update_post(postId: UUID, title: Optional[str] = None, description: Optional[str] = None, pathToImage: Optional[str] = None):
    await filter_updates(postId, {"title": title, "description": description, "pathToImage": pathToImage})
    return {"message": f"Post {postId} has been updated."}