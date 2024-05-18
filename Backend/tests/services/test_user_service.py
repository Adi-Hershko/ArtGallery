import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.user_service import UserService
from app.dals.user_dal import UserDal
from app.pydantic_models.user_models.user_request_model import UserBaseRequestModel
from app.pydantic_models.user_models.user_response_model import UserBaseResponseModel
from app.DB.models import User
from app.exceptions import UserAlreadyExist, OperationError, UserNotFoundException, PasswordNotMatchException

# Test fixtures
# Global variables for use in multiple tests
test_user = UserBaseRequestModel(username="johndoe", password="securepassword123")
mock_user_dal = AsyncMock(spec=UserDal)


@pytest.fixture
def user_service():    
    return UserService(user_dal=mock_user_dal)


@pytest.mark.asyncio
@patch('app.services.user_service.bcrypt')
async def test_create_user_successfully(mock_bcrypt, user_service):
    mock_bcrypt.gensalt.return_value = b'salt'
    mock_bcrypt.hashpw.return_value = b'hashed_password'

    await user_service.create_user(test_user)

    # Validate add_user was called with correct arguments
    assert mock_user_dal.add_user.call_args is not None
    user_arg = mock_user_dal.add_user.call_args[0][0]
    assert isinstance(user_arg, User), "Argument must be an instance of User model"
    assert user_arg.username == test_user.username, "Username must match"
    assert user_arg.password == b'hashed_password', "Passwords must be hashed"


@pytest.mark.asyncio
async def test_create_user_already_exists(user_service):
    mock_user_dal.add_user.side_effect = UserAlreadyExist("User already exists.")

    with pytest.raises(UserAlreadyExist):
        await user_service.create_user(test_user)


@pytest.mark.asyncio
@patch('app.services.user_service.bcrypt')
async def test_create_user_operation_error(mock_bcrypt, user_service):
    mock_bcrypt.gensalt.return_value = b'salt'
    mock_bcrypt.hashpw.return_value = b'hashed_password'
    mock_user_dal.add_user.side_effect = Exception("Unexpected error")

    with pytest.raises(OperationError):
        await user_service.create_user(test_user)


@pytest.mark.asyncio
@patch('app.services.user_service.bcrypt')
async def test_validate_user_not_found(mock_bcrypt, user_service):
    mock_user_dal.find_user.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.validate_user(test_user)


@pytest.mark.asyncio
@patch('app.services.user_service.bcrypt')
async def test_validate_user_password_not_match(mock_bcrypt, user_service):
    fetched_user = MagicMock()
    fetched_user.password = b'hashed_password'
    mock_user_dal.find_user.return_value = fetched_user
    mock_bcrypt.checkpw.return_value = False

    with pytest.raises(PasswordNotMatchException):
        await user_service.validate_user(test_user)


@pytest.mark.asyncio
@patch('app.services.user_service.bcrypt')
async def test_validate_user_success(mock_bcrypt, user_service):
    fetched_user = MagicMock()
    fetched_user.username = test_user.username
    fetched_user.password = b'hashed_password'
    mock_user_dal.find_user.return_value = fetched_user
    mock_bcrypt.checkpw.return_value = True

    result = await user_service.validate_user(test_user)
    
    assert isinstance(result, UserBaseResponseModel), "Result must be an instance of UserBaseResponseModel"
    assert result.username == test_user.username, "Usernames must match"
    assert result.is_active == True, "User should be active"