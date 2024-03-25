from unittest.mock import Mock, AsyncMock

import pytest
from jose import JWSError, jwt

from app.config.models import AuthConfig
from app.routes.middlewares.auth_middleware import AccessTokenCreator, AuthMiddleware


def test_create_access_token_valid_username_default_expiration():
    # Arrange
    config = AuthConfig("secret_key", "HS256")
    access_token_creator = AccessTokenCreator(config)
    username = "test_user"

    # Act
    access_token = access_token_creator.create_access_token(username)

    # Assert
    assert isinstance(access_token, str)
    assert access_token != ""


def test_create_access_token_invalid_algorithm_valid_username():
    # Arrange
    config = AuthConfig("secret_key", "invalid_algorithm")
    access_token_creator = AccessTokenCreator(config)
    username = "test_user"

    # Assert
    with pytest.raises(JWSError):
        access_token_creator.create_access_token(username)


@pytest.mark.asyncio
async def test_middleware_decodes_jwt_and_sets_user():
    app = Mock()
    secret_key = "secret"
    algorithm = "HS256"
    exclude_paths = None
    middleware = AuthMiddleware(app, secret_key, algorithm, exclude_paths)
    request = Mock()
    request.url.path = "/test"
    credentials = "valid_token"
    request.cookies.get.return_value = credentials
    payload = {"sub": "user_id"}
    jwt.decode = Mock(return_value=payload)
    next_function = AsyncMock()

    await middleware.dispatch(request, next_function)


@pytest.mark.asyncio
async def test_middleware_decodes_jwt_and_sets_user_token_does_not_exists():
    app = Mock()
    secret_key = "secret"
    algorithm = "HS256"
    exclude_paths = None
    middleware = AuthMiddleware(app, secret_key, algorithm, exclude_paths)
    request = Mock()
    request.cookies.get.return_value = {}
    request.url.path = "/test"
    payload = {"sub": "user_id"}
    jwt.decode = Mock(return_value=payload)
    next_function = AsyncMock()

    response = await middleware.dispatch(request, next_function)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_middleware_decodes_jwt_and_sets_user_jwse_error():
    app = Mock()
    secret_key = "secret"
    algorithm = "HS256"
    exclude_paths = None
    middleware = AuthMiddleware(app, secret_key, algorithm, exclude_paths)
    request = Mock()
    request.url.path = "/test"
    credentials = "valid_token"
    request.cookies.get.return_value = credentials
    jwt.decode = Mock(side_effect=JWSError)
    next_function = AsyncMock()

    response = await middleware.dispatch(request, next_function)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_middleware_decodes_jwt_and_sets_user_jwt_error():
    app = Mock()
    secret_key = "secret"
    algorithm = "HS256"
    exclude_paths = None
    middleware = AuthMiddleware(app, secret_key, algorithm, exclude_paths)
    request = Mock()
    request.url.path = "/test"
    credentials = "valid_token"
    request.cookies.get.return_value = credentials
    jwt.decode = Mock(side_effect=jwt.JWTError)
    next_function = AsyncMock()

    response = await middleware.dispatch(request, next_function)
    assert response.status_code == 401