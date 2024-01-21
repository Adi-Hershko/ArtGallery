from fastapi import FastAPI
from app.routes.user_controller import user_controller_router
from app.routes.post_controller import post_controller_router

app = FastAPI()

app.include_router(user_controller_router)
app.include_router(post_controller_router)
