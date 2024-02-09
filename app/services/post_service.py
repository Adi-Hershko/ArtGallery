from app.dals.post_dal import *
from app.dals.user_dal import find_user
from app.exceptions import UserNotFoundException
from ..pydantic_models.post_models.post_request_model import *
from app.pydantic_models.post_models.post_response_model import *


async def get_feed(feed_reqs: PostFeedRequestModel):
    not_nullables_conditions = {key: value for key, value in feed_reqs.convert_to_dict().items() if value is not None}
    posts = await get_all_posts(not_nullables_conditions)

    return list(map(
        lambda post: PostGetResponseModel(
            username=post.username,
            postId=post.postId,
            title=post.title,
            description=post.description,
            pathToImage=post.pathToImage,
            insertionTime=post.insertionTime
        ), posts
    ))


async def create_post(post: PostUploadRequestModel):
    user = await find_user(post.username)
    if user is None:
        raise UserNotFoundException("User not found.")
    print("User found", user)
    await add_post(
        Post(username=post.username, title=post.title, description=post.description, pathToImage=post.pathToImage)
    )


async def find_post_and_delete(post: PostIdSearchRequestModel):
    is_deleted = await delete_post_in_db(post.postId)
    if is_deleted is False:
        raise PostNotFoundException("Post not found.")
    print(f"Post {post.postId} has been set inactive.")


async def find_post_and_update(post: PostUpdateRequestModel):
    not_nullables_updates = {key: value for key, value in post.convert_to_dict().items() if value is not None}
    rows_affected = await update_post_in_db(post.postId, not_nullables_updates)

    if rows_affected == 0:
        raise PostNotFoundException("Post not found.")
