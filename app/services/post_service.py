from app.dals.post_dal import *
from app.dals.user_dal import find_user
from app.exceptions import UserNotFoundException
from ..pydantic_models.post_models.post_request_model import *
from ..pydantic_models.user_models.user_request_model import UserSearchRequestModel


async def get_feed(feedReqs: PostFeedRequestModel):
    not_nullables_conditions = {key: value for key, value in feedReqs.convert_to_dict().items() if value is not None}
    return await get_all_posts(not_nullables_conditions)

async def create_post(post: PostUploadRequestModel):
    user = await find_user(UserSearchRequestModel(username=post.username))
    if user is None:
        raise UserNotFoundException("User not found.")
    print("User found", user)
    await add_post(post)

async def find_post_and_delete(post: PostIdSearchRequestModel):
    is_deleted = await delete_post_in_db(post)
    if is_deleted is False:
        raise PostNotFoundException("Post not found.")
    print(f"Post {post.postId} has been set inactive.")

async def find_post_and_update(post: PostUpdateRequestModel):
    rows_affected = await update_post_in_db(post)
    if rows_affected == 0:
        raise PostNotFoundException("Post not found.")