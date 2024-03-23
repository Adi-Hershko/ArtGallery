from fastapi import APIRouter, Depends
from app.services.post_service import *
from app.pydantic_models.post_models.post_request_model import *
from app.routes import routes_path

@inject
class PostController:
    def __init__(self, post_service: PostService):
        self.router = APIRouter()
        self.post_service = post_service
        self.register_routes()

    def register_routes(self):
        self.router.get(routes_path.GET_POSTS, tags=["Posts"])(self.get_posts)
        self.router.post(routes_path.UPLOAD_POST, tags=["Posts"])(self.upload_post)
        self.router.delete(routes_path.DELETE_POST, tags=["Posts"])(self.delete_post)
        self.router.put(routes_path.UPDATE_POST, tags=["Posts"])(self.update_post)

    async def get_posts(self, feed_reqs: PostFeedRequestModel = Depends(PostFeedRequestModel)) -> List[PostGetResponseModel]:
        return await self.post_service.get_feed(feed_reqs)

    # TODO: figure out how to pass the image from the front to the back as body
    async def upload_post(self, post: PostUploadRequestModel = Depends(PostUploadRequestModel)) -> PostGetResponseModel:        
        return await self.post_service.create_post(post)        

    async def delete_post(self, post: PostIdSearchRequestModel  = Depends(PostIdSearchRequestModel)) -> dict:
        await self.post_service.find_post_and_delete(post)
        return {"message": f"Post {post.postId} has been deleted."}

    async def update_post(self, post: PostUpdateRequestModel = Depends(PostUpdateRequestModel)) -> PostGetResponseModel:
        return await self.post_service.find_post_and_update(post)
        
