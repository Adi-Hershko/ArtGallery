from fastapi import APIRouter, Depends
from typing import Optional
from Backend.app.services.post_service import *
from ..pydantic_models.post_models.post_request_model import *
from uuid import UUID

post_controller_router = APIRouter()

@post_controller_router.get("/posts", tags=["Posts"])
async def get_posts(feedReqs: PostFeedRequestModel = Depends(PostFeedRequestModel)):
    return await get_feed(feedReqs)


@post_controller_router.post("/upload-post", tags=["Posts"])
async def upload_post(post: PostUploadRequestModel = Depends(PostUploadRequestModel)):
    await create_post(post)
    return {"message": f"{post.title} has been uploaded."}


@post_controller_router.delete("/delete-post", tags=["Posts"])
async def delete_post(post: PostIdSearchRequestModel  = Depends(PostIdSearchRequestModel)):
    await find_post_and_delete(post)
    return {"message": f"Post {post.postId} has been deleted."}


@post_controller_router.put("/update-post", tags=["Posts"])
async def update_post(post: PostUpdateRequestModel = Depends(PostUpdateRequestModel)):
    await find_post_and_update(post)
    return {"message": f"Post {post.postId} has been updated."}
