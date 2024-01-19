from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.openapi.models import Response

from app.routes.middlewares.auth_middleware import validate_auth

post_controller = APIRouter()


@post_controller.post("/create-post", tags=["Posts"])
async def create_post(title: str, content: str, dependency=Depends(validate_auth)) -> dict:
    return {"message": "Post created successfully"}

