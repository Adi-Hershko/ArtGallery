from app.dals.post_dal import *
from app.dals.user_dal import UserDal
from app.exceptions import UserNotFoundException
from app.pydantic_models.post_models.post_response_model import *
from app.services.os_service import OsService


@inject
class PostService:
    def __init__(self, post_dal: PostDal, user_dal: UserDal, os_service: OsService):
        self.post_dal = post_dal
        self.user_dal = user_dal
        self.os_service = os_service

    async def get_feed(self, feed_reqs: PostFeedRequestModel):
        not_nullables_conditions = {key: value for key, value in feed_reqs.convert_to_dict().items() if value is not None and value.strip() != ''}
        posts = await self.post_dal.get_all_posts(not_nullables_conditions)

        return list(map(
            lambda post: PostGetResponseModel(
                username=post.username,
                postId=post.post_id,
                title=post.title,
                description=post.description,
                path_to_image=post.path_to_image,
                insertionTime=post.insertion_time,
                path_to_thumbnail=post.path_to_thumbnail
            ), posts
        ))

    async def create_post(self, post: PostUploadRequestModel):
        user = await self.user_dal.find_user(post.username)
        if user is None:
            raise UserNotFoundException("User not found.")
        else:
            (path_to_image, path_to_thumbnail) = await self.os_service.upload_image_and_thumbnail(
                post.Image, post.title, post.username
            )

            await self.post_dal.add_post(
                Post(username=post.username,
                     title=post.title,
                     description=post.description,
                     path_to_image=path_to_image,
                     path_to_thumbnail=path_to_thumbnail
                     )
            )

    async def find_post_and_delete(self, post: PostIdSearchRequestModel):
        await self.post_dal.delete_post_in_db(post.postId)

    async def find_post_and_update(self, post: PostUpdateRequestModel):
        not_nullables_updates = {key: value for key, value in post.convert_to_dict().items() if value is not None}
        await self.post_dal.update_post_in_db(post.postId, not_nullables_updates)
