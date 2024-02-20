import pytest
from unittest.mock import Mock, AsyncMock

from fastapi import UploadFile

from app.DB.models import Post, User
from app.dals.post_dal import PostDal
from app.dals.user_dal import UserDal
from app.exceptions import OperationError, UserNotFoundException
from app.services.os_service import OsService
from app.services.post_service import PostService

# file: UploadFile, title: str, username: str


@pytest.mark.asyncio
async def test_create_post_():
    mock_user_dal = UserDal
    mock_post_dal = PostDal
    mock_os_service = OsService
    mock_file = Mock(UploadFile)
    mock_user = Mock(User)
    mock_post = Mock(Post)

    mock_user_dal.find_user = AsyncMock(side_effect=lambda username: mock_user if username == "abc" else None)
    mock_post_dal.add_post = AsyncMock()
    mock_os_service.upload_image_and_thumbnail = AsyncMock(
        side_effect=lambda file, title, username: ("path", "thumbnail/path")
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


def raise_operation_error(_):
    raise OperationError()


def return_none(_):
    return None
