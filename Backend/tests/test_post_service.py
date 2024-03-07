import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import UploadFile
from app.pydantic_models.post_models.post_response_model import PostGetResponseModel
from app.pydantic_models.post_models.post_request_model import PostIdSearchRequestModel, PostUpdateRequestModel, PostFeedRequestModel
from app.DB.models import Post, User
from app.dals.post_dal import PostDal
from app.dals.user_dal import UserDal
from app.exceptions import OperationError, UserNotFoundException
from app.services.os_service import OsService
from app.services.post_service import PostService
from uuid import uuid4
from datetime import datetime


@pytest.mark.asyncio
async def test_get_feed_with_empty_conditions():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = OsService
    mock_feed_reqs = Mock(PostFeedRequestModel, convert_to_dict=Mock(return_value={}))

    mock_post_dal.get_all_posts = AsyncMock()

    mock_post_1 = Mock(Post, 
                       post_id=uuid4(),
                       username="user1", 
                       title="title1", 
                       description="desc1", 
                       path_to_image="http://example.com/image1.jpg", 
                       insertion_time=datetime.now()
                       )                       
    mock_post_2 = Mock(Post, 
                       post_id=uuid4(), 
                       username="user2", 
                       title="title2", 
                       description="desc2", 
                       path_to_image="http://example.com/image2.jpg", 
                       insertion_time=datetime.now()
                       )

    mock_posts = [mock_post_1, mock_post_2]

    mock_post_dal.get_all_posts.return_value = mock_posts

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    result_posts = await post_service.get_feed(mock_feed_reqs)

    assert len(result_posts) == 2
    assert all(isinstance(post, PostGetResponseModel) for post in result_posts)
    mock_post_dal.get_all_posts.assert_called_once_with({})


@pytest.mark.asyncio
async def test_get_feed_with_emtpy_string_conditions():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = OsService
    mock_feed_reqs = Mock(PostFeedRequestModel, convert_to_dict=Mock(return_value={'username': ''}))

    mock_post_dal.get_all_posts = AsyncMock()

    mock_post_1 = Mock(Post, 
        post_id=uuid4(), 
        username="user1", 
        title="title1", 
        description="desc1", 
        path_to_image="http://example.com/image1.jpg", 
        insertion_time=datetime.now()
    )
    mock_post_2 = Mock(Post, 
        post_id=uuid4(), 
        username="user2", 
        title="title2", 
        description="desc2", 
        path_to_image="http://example.com/image2.jpg", 
        insertion_time=datetime.now()
    )

    mock_posts = [mock_post_1, mock_post_2]

    mock_post_dal.get_all_posts.return_value = mock_posts

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    result_posts = await post_service.get_feed(mock_feed_reqs)

    assert len(result_posts) == 2
    assert all(isinstance(post, PostGetResponseModel) for post in result_posts)
    mock_post_dal.get_all_posts.assert_called_once_with({})


@pytest.mark.asyncio
async def test_get_feed_with_non_empty_conditions():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = OsService

    mock_post_dal.get_all_posts = AsyncMock()
    
    feed_requirements = {'username': 'user1'}
    mock_feed_reqs = Mock(PostFeedRequestModel, convert_to_dict=Mock(return_value=feed_requirements))

    # Mock posts, including both those that meet the feed requirements and those that do not
    mock_filtered_post = Mock(Post, 
            post_id=uuid4(), 
            username="user1", 
            title="Filtered Post Title", 
            description="Filtered post description", 
            path_to_image="http://example.com/filtered_image.jpg", 
            insertion_time=datetime.now()
    )
    mock_unfiltered_post = Mock(Post, 
        post_id=uuid4(), 
        username="user2", 
        title="Unfiltered Post Title", 
        description="Unfiltered post description", 
        path_to_image="http://example.com/unfiltered_image.jpg", 
        insertion_time=datetime.now()
    )

    # Return both filtered and unfiltered posts from the DAL
    mock_posts = [mock_filtered_post, mock_unfiltered_post]

    mock_post_dal.get_all_posts.return_value = [mock_filtered_post]

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    result_posts = await post_service.get_feed(mock_feed_reqs)

    # Assertions to ensure only the filtered post is returned
    assert len(result_posts) == 1
    assert all(isinstance(post, PostGetResponseModel) for post in result_posts)
    assert result_posts[0].username == feed_requirements['username']
    mock_post_dal.get_all_posts.assert_called_once_with(feed_requirements)


@pytest.mark.asyncio
async def test_create_post():
    mock_user_dal = UserDal
    mock_post_dal = PostDal
    mock_os_service = OsService
    mock_file = Mock(UploadFile)
    mock_user = Mock(User)
    mock_post = Mock(Post)

    mock_user_dal.find_user = AsyncMock(side_effect=lambda username: mock_user if username == "abc" else None)
    mock_post_dal.add_post = AsyncMock()
    mock_os_service.upload_image_and_thumbnail = AsyncMock(
        side_effect=lambda file, title, username: "path"
        if username == "abc" and title == "title" and file == mock_file else None
    )

    mock_post.username = "abc"
    mock_post.title = "title"
    mock_post.Image = mock_file
    mock_post.description = "test description"

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)

    await post_service.create_post(mock_post)

    mock_post_dal.add_post.assert_called_once()


@pytest.mark.asyncio
async def test_create_post_user_is_none_get_user_not_found_exception():
    mock_user_dal = UserDal
    mock_post_dal = PostDal
    mock_os_service = OsService
    mock_file = Mock(UploadFile)
    mock_post = Mock(Post)

    mock_user_dal.find_user = AsyncMock(side_effect=return_none)

    mock_post.username = "abc"
    mock_post.title = "title"
    mock_post.Image = mock_file
    mock_post.description = "test description"

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    with pytest.raises(UserNotFoundException):
        await post_service.create_post(mock_post)


@pytest.mark.asyncio
async def test_find_post_and_update_update_reqs_not_empty():
    mock_post_dal = PostDal 
    mock_user_dal = UserDal
    mock_os_service = OsService
    mock_post_update_req = Mock(PostUpdateRequestModel, postId="id1", convert_to_dict=Mock(return_value={'title': 'updated_title'}))

    mock_post_dal.update_post_in_db = AsyncMock()

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    await post_service.find_post_and_update(mock_post_update_req)

    mock_post_dal.update_post_in_db.assert_called_once_with("id1", {'title': 'updated_title'})


@pytest.mark.asyncio
async def test_find_post_and_update_update_reqs_is_empty():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = OsService
    mock_post_update_req = Mock(PostUpdateRequestModel, postId="id1", convert_to_dict=Mock(return_value={}))

    mock_post_dal.update_post_in_db = AsyncMock()

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    await post_service.find_post_and_update(mock_post_update_req)

    mock_post_dal.update_post_in_db.assert_called_once_with("id1", {})


@pytest.mark.asyncio
async def test_find_post_and_delete():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = OsService
    mock_post_id_search_req = Mock(PostIdSearchRequestModel, postId="id1")

    mock_post_dal.delete_post_in_db = AsyncMock()

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    await post_service.find_post_and_delete(mock_post_id_search_req)

    mock_post_dal.delete_post_in_db.assert_called_once_with("id1")


def raise_operation_error(_):
    raise OperationError()


def return_none(_):
    return None
