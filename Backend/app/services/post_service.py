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

    async def get_feed(self, feed_reqs: PostFeedRequestModel) -> List[PostGetResponseModel]:
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
            ), posts
        ))

    async def create_post(self, post: PostUploadRequestModel) -> PostGetResponseModel:
        user = await self.user_dal.find_user(post.username)
        if user is None:
            raise UserNotFoundException("User not found.")        
        if post.description is not None and post.description.strip() == '':
            post.description = None        
        path_to_image = await self.os_service.upload_image(post.Image, post.title, post.username)

        new_post = await self.post_dal.add_post(
            Post(username=post.username,
                    title=post.title,
                    description=post.description,
                    path_to_image=path_to_image,                    
                    )
        )
        return PostGetResponseModel(
            postId=new_post.post_id,
            username=new_post.username,
            title=new_post.title,
            description=new_post.description,
            path_to_image=new_post.path_to_image,
            insertionTime=new_post.insertion_time
        )

    async def find_post_and_delete(self, post: PostIdSearchRequestModel):
        await self.post_dal.delete_post_in_db(post.postId)

    async def find_post_and_update(self, post: PostUpdateRequestModel) -> PostGetResponseModel:        
        updates = {}
        if post.title is not None and post.title.strip() != '':
            updates['title'] = post.title
        if post.description is not None and post.description.strip() != '':
            updates['description'] = post.description        
        if post.Image is not None:            
            updates['path_to_image'] = await self.os_service.update_image(post.Image, post.path_to_image, post.username)
        updated_post = await self.post_dal.update_post_in_db(post.postId, updates)
        return PostGetResponseModel(
            postId=updated_post.post_id,
            username=updated_post.username,
            title=updated_post.title,
            description=updated_post.description,
            path_to_image=updated_post.path_to_image,            
            insertionTime=updated_post.insertion_time
        )
