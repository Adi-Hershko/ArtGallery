from fastapi.responses import JSONResponse
from jose import jwt

from app.exceptions import *

async def default_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

async def user_not_found_exception_handler(request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": "User not found"}
    )

async def password_not_match_exception_handler(request, exc: PasswordNotMatchException):
    return JSONResponse(
        status_code=401,
        content={"message": "Unauthorized"}
    )

async def invalid_auth_handler(request, exc: jwt.JWTError):
    return JSONResponse(
        status_code=401,
        content={"message": "Unauthorized"}
    )

async def post_not_found_exception_handler(request, exc: PostNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": "Post not found"}
    )

async def feed_not_found_exception_handler(request, exc: FeedNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": "Feed not found"}
    )

async def operation_error_exception_handler(request, exc: OperationError):
    return JSONResponse(
        status_code=500,
        content={"message": "Operation error"}
    )


async def user_already_exist_exception_handler(request, exc: UserAlreadyExist):
    return JSONResponse(
        status_code=409,
        content={"message": "User already exists"}
    )

async def password_too_short_exception_handler(request, exc: PasswordTooShort):
    return JSONResponse(
        status_code=400,
        content={"message": "Password too short, must be at least 6 characters"}
    )

async def password_too_long_exception_handler(request, exc: PasswordTooLong):
    return JSONResponse(
        status_code=400,
        content={"message": "Password too long, must be at most 50 characters"}
    )

async def username_too_short_exception_handler(request, exc: UsernameTooShort):
    return JSONResponse(
        status_code=400,
        content={"message": "Username too short, must be at least 3 characters"}
    )

async def username_too_long_exception_handler(request, exc: UsernameTooLong):
    return JSONResponse(
        status_code=400,
        content={"message": "Username too long, must be at most 50 characters"}
    )