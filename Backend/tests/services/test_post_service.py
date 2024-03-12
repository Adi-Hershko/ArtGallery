import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import UploadFile
from app.exceptions import PostNotFoundException
from app.services.post_service import PostService
from app.pydantic_models.post_models.post_request_model import PostFeedRequestModel, PostUploadRequestModel, PostIdSearchRequestModel, PostUpdateRequestModel
from app.pydantic_models.post_models.post_response_model import PostGetResponseModel
from app.exceptions import UserNotFoundException
from app.DB.models import User, Post
from datetime import datetime
from app.dals.post_dal import PostDal
from app.dals.user_dal import UserDal
from app.services.os_service import OsService
from uuid import uuid4


# Mocks setup
mock_post_dal = Mock(spec=PostDal)
mock_user_dal = Mock(spec=UserDal)
mock_os_service = Mock(spec=OsService)

# Shared post instances for testing
mock_post_1 = Mock(spec=Post, post_id=uuid4(), username="user1", title="title1", description="desc1", path_to_image="http://example.com/image1.jpg", insertion_time=datetime.now(), is_active=True)
mock_post_2 = Mock(spec=Post, post_id=uuid4(), username="user2", title="title2", description="desc2", path_to_image="http://example.com/image2.jpg", insertion_time=datetime.now(), is_active=True)

# Create a single instance of PostService for all tests
post_service = PostService(mock_post_dal, mock_user_dal, mock_os_service)


@pytest.mark.asyncio
@pytest.mark.parametrize("feed_reqs,expected_result", [
    ({}, [mock_post_1, mock_post_2]),  # Test with empty conditions returns all posts
    ({'username': 'nonexistent'}, []),  # Test with username that doesn't match any post
    ({'username': 'user1', 'title': 'title1'}, [mock_post_1]),  # Test with matching conditions
    ({'username': 'user3'}, []),  # Test with username that doesn't exist
])
async def test_get_feed_varied_conditions(feed_reqs, expected_result):
    mock_post_dal.get_all_posts = AsyncMock(return_value=expected_result)
    mock_feed_reqs = PostFeedRequestModel(**feed_reqs)  # Adjusted to directly create an instance
    result_posts = await post_service.get_feed(mock_feed_reqs)
    assert len(result_posts) == len(expected_result), "The number of returned posts should match the expected result."
    mock_post_dal.get_all_posts.assert_called_once_with(feed_reqs)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_data,user_exists,expected_exception", [    
    ({"username": "user1", "title": "New Post", "description": "Content", "Image": Mock(spec=UploadFile)}, True, None),  # Normal case
    ({"username": "user3", "title": "New Post", "description": "Content", "Image": Mock(spec=UploadFile)}, False, UserNotFoundException),  # User doesn't exist
])
async def test_create_post_varied_conditions(input_data, user_exists, expected_exception):
    mock_user_dal.find_user = AsyncMock(return_value=mock_post_1 if user_exists else None)
    mock_os_service.upload_image = AsyncMock(return_value="http://example.com/image.jpg")
    mock_post_dal.add_post = AsyncMock(return_value=mock_post_1)
    post_upload_request_model = PostUploadRequestModel(**input_data)

    if expected_exception:
        with pytest.raises(expected_exception):
            await post_service.create_post(post_upload_request_model)
    else:
        result = await post_service.create_post(post_upload_request_model)
        assert isinstance(result, PostGetResponseModel), "Result should be an instance of PostGetResponseModel."


@pytest.mark.asyncio
@pytest.mark.parametrize("post_id, post_exists, expected_exception", [
    (mock_post_1.post_id, True, None),  # Existing post ID
    (uuid4(), False, PostNotFoundException),  # Non-existing post ID
])
async def test_delete_post(post_id, post_exists, expected_exception):            
    if expected_exception:
        with pytest.raises(expected_exception, match="Post not found"):
            mock_post_dal.delete_post_in_db = AsyncMock(side_effect=PostNotFoundException("Post not found"))
            await post_service.find_post_and_delete(PostIdSearchRequestModel(postId=post_id))
    else:
        mock_post_dal.delete_post_in_db = AsyncMock()
        await post_service.find_post_and_delete(PostIdSearchRequestModel(postId=post_id))
        mock_post_dal.delete_post_in_db.assert_called_once_with(post_id)


pytest.mark.asyncio
@pytest.mark.parametrize("update_reqs, user_exists, expected_changes, expected_exception", [
    # Update all fields
    (
        {'title': 'New Title', 'description': 'Updated Description', 'Image': Mock(spec=UploadFile)},
        True,
        {'title': 'New Title', 'description': 'Updated Description', 'path_to_image': 'updated/path.png'},
        None
    ),
    # No updates provided, return current post
    ({}, True, {}, None),
    # User does not exist
    ({'title': 'New Title'}, False, {}, UserNotFoundException),
    # Update image only
    ({'Image': Mock(spec=UploadFile)}, True, {'path_to_image': 'updated/path.png'}, None),
])
async def test_find_post_and_update_varied_conditions(update_reqs, user_exists, expected_changes, expected_exception):
    mock_user_dal.find_user = AsyncMock(return_value=User() if user_exists else None)
    mock_os_service.update_image = AsyncMock(return_value="updated/path.png" if 'Image' in update_reqs else mock_post_1.path_to_image)
        
    updated_post = Mock(spec=Post, post_id=mock_post_1.post_id, username=mock_post_1.username, **expected_changes)

    mock_post_dal.update_post_in_db = AsyncMock(return_value=updated_post)
    mock_post_update_req = PostUpdateRequestModel(postId=mock_post_1.post_id, path_to_image=mock_post_1.path_to_image, username=mock_post_1.username, **update_reqs)

    if expected_exception:
        with pytest.raises(expected_exception):
            await post_service.find_post_and_update(mock_post_update_req)
    else:
        result = await post_service.find_post_and_update(mock_post_update_req)
        assert isinstance(result, PostGetResponseModel), "Result should be an instance of PostGetResponseModel."
        assert result.postId == mock_post_1.post_id, "Post ID should remain unchanged."
        assert result.username == mock_post_1.username, "Username should remain unchanged."
        for field, expected_value in expected_changes.items():
            assert getattr(result, field) == expected_value, f"Field '{field}' should be updated to '{expected_value}'."
        if update_reqs:
            mock_post_dal.update_post_in_db.assert_called_once_with(mock_post_1.post_id, expected_changes)
        else:
            mock_post_dal.update_post_in_db.assert_called_once_with(mock_post_1.post_id, {})