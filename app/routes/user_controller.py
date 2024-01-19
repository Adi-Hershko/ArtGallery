from fastapi import APIRouter, HTTPException
from app.services.user_service import create_user, validate_user
from app.exceptions import UserNotFoundException

user_controller_router = APIRouter()


@user_controller_router.post("/sign-up", tags=["Users"])
async def sign_up(username: str, password: str) -> dict:
    rows_affected = create_user(username, password)
    if rows_affected == 1:
        return {"message": f"{username} has been signed up."}
    else:
        return {"message": "Something went wrong"}


@user_controller_router.post("/sign-in", tags=["Users"])
async def sign_in(username: str, password: str) -> dict:
    try:
        is_valid = validate_user(username, password)
        if is_valid:
            return {"message": f"{username} has been signed in."}
        else:
            raise HTTPException(status_code=401, detail="Invalid request")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")


@user_controller_router.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Welcome to Art Gallery!"}

