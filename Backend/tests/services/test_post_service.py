import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import UploadFile
from app.pydantic_models.post_models.post_response_model import PostGetResponseModel
from app.pydantic_models.post_models.post_request_model import PostIdSearchRequestModel, PostUpdateRequestModel, PostFeedRequestModel, PostUploadRequestModel
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

    mock_file = Mock(spec=UploadFile)
    mock_user = Mock(spec=User)
    mock_post_id = uuid4()
    mock_insertion_time = datetime.now()
    mock_post = Post(post_id=mock_post_id, username="johndoe", title="My new post", description="This is a new post", path_to_image="path/to/image.jpg", insertion_time=mock_insertion_time, is_active=True)
        
    post_upload_request_model = PostUploadRequestModel(username="johndoe", title="My new post", description="This is a new post", Image=mock_file)
        
    mock_user_dal.find_user = AsyncMock(return_value=lambda: mock_user if mock_user.username == "johndoe" else None)  
    mock_post_dal.add_post = AsyncMock(return_value=mock_post)
    mock_os_service.upload_image = AsyncMock(return_value="path/to/image.jpg")
    
    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
 
    new_post = await post_service.create_post(post_upload_request_model)
        
    assert new_post.postId == mock_post_id
    assert new_post.path_to_image == "path/to/image.jpg"
    assert new_post.username == "johndoe"
    assert new_post.title == "My new post"
    assert new_post.description == "This is a new post"
    assert new_post.insertionTime == mock_insertion_time    
    
    mock_user_dal.find_user.assert_called_once_with("johndoe")
    mock_os_service.upload_image.assert_called_once()
    mock_post_dal.add_post.assert_called_once()


@pytest.mark.asyncio
async def test_create_post_user_is_none_get_user_not_found_exception():
    mock_user_dal = UserDal
    mock_post_dal = PostDal
    mock_os_service = Mock(OsService)
    mock_file = Mock(UploadFile)
    mock_post = Mock(Post)

    mock_user_dal.find_user = AsyncMock(return_value=None)

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
    mock_os_service = Mock(OsService)

    mock_user = Mock(User, username="johndoe")
    mock_file = Mock(UploadFile)
    mock_post_id = uuid4()
    mock_insertion_time = datetime.now()
    mock_post = Mock(Post, post_id=mock_post_id, username="johndoe", title="Updated Title", description="Updated Description", path_to_image="updated/path.png", insertion_time=mock_insertion_time, is_active=True)    
    mock_post_update_req = Mock(PostUpdateRequestModel, postId=mock_post_id, path_to_image="current/path.jpg" ,username="johndoe", title="Updated Title", description="Updated Description", Image=mock_file)

    mock_user_dal.find_user = AsyncMock(return_value=mock_user)
    mock_os_service.update_image = AsyncMock(return_value="updated/path.png")

    mock_post_dal.update_post_in_db = AsyncMock(return_value=mock_post)

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    updated_post = await post_service.find_post_and_update(mock_post_update_req)

    assert updated_post.postId == mock_post_id
    assert updated_post.path_to_image == "updated/path.png"
    assert updated_post.username == "johndoe"
    assert updated_post.title == "Updated Title"
    assert updated_post.description == "Updated Description"
    assert updated_post.insertionTime == mock_insertion_time

    mock_user_dal.find_user.assert_called_once_with("johndoe")
    mock_os_service.update_image.assert_called_once_with(mock_file, "current/path.jpg", "johndoe")
    mock_post_dal.update_post_in_db.assert_called_once_with(mock_post_id, {'title': 'Updated Title', 'description': 'Updated Description', 'path_to_image': 'updated/path.png'})


@pytest.mark.asyncio
async def test_find_post_and_update_update_reqs_is_empty():
    mock_post_dal = PostDal
    mock_user_dal = UserDal
    mock_os_service = Mock(OsService)
    
    mock_user = Mock(User, username="johndoe")
    mock_user_dal.find_user = AsyncMock(return_value=mock_user)

    mock_post_id = uuid4()
    mock_insertion_time = datetime.now()
    mock_post = Mock(Post, post_id=mock_post_id, username="johndoe", title="Same Title", description="Same Description", path_to_image="same/path.png", insertion_time=mock_insertion_time, is_active=True)

    mock_post_update_req = Mock(PostUpdateRequestModel, postId=mock_post_id, path_to_image="same/path.png", username="johndoe", title="", description="", Image=None)

    mock_post_dal.update_post_in_db = AsyncMock(return_value=mock_post)

    post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)
    updated_post = await post_service.find_post_and_update(mock_post_update_req)    

    assert updated_post.postId == mock_post_id
    assert updated_post.path_to_image == "same/path.png"
    assert updated_post.username == "johndoe"
    assert updated_post.title == "Same Title"
    assert updated_post.description == "Same Description"
    assert updated_post.insertionTime == mock_insertion_time

    mock_user_dal.find_user.assert_called_once_with("johndoe") 
    # update_image should not be called since the image is not being updated
    mock_os_service.update_image.assert_not_called()
    mock_post_dal.update_post_in_db.assert_awaited_once_with(mock_post_id, {})


    


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

def return_none():
    return None