from fastapi import FastAPI
from app.routes.user_controller import user_controller_router
from app.routes.post_controller import post_controller_router
from app.exceptions import *
from app.routes.error_handling import *

app = FastAPI()

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(PasswordNotMatchException, password_not_match_exception_handler)
app.add_exception_handler(Exception, default_exception_handler)
app.add_exception_handler(PostNotFoundException, post_not_found_exception_handler)
app.add_exception_handler(FeedNotFoundException, feed_not_found_exception_handler)
app.add_exception_handler(OperationError, operation_error_exception_handler)

app.include_router(user_controller_router)
app.include_router(post_controller_router)
