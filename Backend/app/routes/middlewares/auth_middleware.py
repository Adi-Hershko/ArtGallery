from fastapi import Request, Depends
from Backend.app.exceptions import UserNotFoundException


async def validate_auth(request: Request):
    body = await request.json()
    if len(body['title']) > 5:
        raise UserNotFoundException()
