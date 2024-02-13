import bootstrap

bootstrap.bootstrap_di()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.app.routes.user_controller import user_controller_router
from Backend.app.routes.post_controller import post_controller_router
from Backend.app.routes.error_handling import *

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

app.include_router(user_controller_router)
app.include_router(post_controller_router)
