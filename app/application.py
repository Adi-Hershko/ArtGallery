from fastapi import FastAPI, HTTPException, Request
from app.routes.user_controller import user_controller_router
from app.routes.post_controller import post_controller_router
from app.exceptions import UserNotFoundException, PasswordNotMatchException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)}
    )

@app.exception_handler(PasswordNotMatchException)
async def password_not_match_exception_handler(request, exc: PasswordNotMatchException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)}
    )

app.include_router(user_controller_router)
app.include_router(post_controller_router)
