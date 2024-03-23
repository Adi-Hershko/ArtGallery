import app.bootstrap as bootstrap
from app.routes.middlewares.auth_middleware import AccessTokenCreator, AuthMiddleware

bootstrap.bootstrap_di()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_controller import UserController
from app.routes.post_controller import PostController
from app.routes.error_handling import *
from app.config.config import origins, auth_config
from app import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    AuthMiddleware,
    secret_key=auth_config.secret_key,
    algorithm=auth_config.algorithm,
    exclude_paths=["/sign-in", "/sign-up"]
)

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(PasswordNotMatchException, password_not_match_exception_handler)
app.add_exception_handler(Exception, default_exception_handler)
app.add_exception_handler(PostNotFoundException, post_not_found_exception_handler)
app.add_exception_handler(FeedNotFoundException, feed_not_found_exception_handler)
app.add_exception_handler(OperationError, operation_error_exception_handler)
app.add_exception_handler(UserAlreadyExist, user_already_exist_exception_handler)

app.add_exception_handler(PasswordTooShort, password_too_short_exception_handler)
app.add_exception_handler(PasswordTooLong, password_too_long_exception_handler)
app.add_exception_handler(UsernameTooShort, username_too_short_exception_handler)
app.add_exception_handler(UsernameTooLong, username_too_long_exception_handler)

user_controller = UserController()
post_controller = PostController()

app.include_router(user_controller.router)
app.include_router(post_controller.router)
