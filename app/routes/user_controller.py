from fastapi import APIRouter, HTTPException
from app.services.user_service import create_user, validate_user

user_controller_router = APIRouter()

@user_controller_router.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Welcome to Art Gallery!"}


@user_controller_router.post("/sign-up", tags=["Users"])
async def sign_up(username: str, password: str) -> dict:
    await create_user(username, password)    
    return {"message": f"{username} has been signed up."}    
            

@user_controller_router.post("/sign-in", tags=["Users"])
async def sign_in(username: str, password: str) -> dict:
    await validate_user(username, password)
    return {"message": f"{username} has been signed in."}