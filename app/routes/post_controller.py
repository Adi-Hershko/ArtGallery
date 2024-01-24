from fastapi import APIRouter, HTTPException


from app.routes.middlewares.auth_middleware import validate_auth

post_controller_router = APIRouter()


# @post_controller_router.post("/create-post", tags=["Posts"])
# async 