from datetime import timedelta, datetime
from typing import Optional

import jose
from fastapi import Request
from jose import jwt, JWSError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config.models import AuthConfig


def _extract_credentials(request: Request) -> Optional[str]:
    return request.cookies.get("token")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, algorithm: str = "HS256", exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.exclude_paths:
            credentials = _extract_credentials(request)
            if credentials:
                try:
                    payload = jwt.decode(credentials, self.secret_key, algorithms=[self.algorithm])
                    request.state.user = payload.get("sub")
                except jwt.JWTError:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "Unauthorized"}
                    )
                except jose.exceptions.JWSError:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "Unauthorized"}
                    )
            else:
                return JSONResponse(
                        status_code=401,
                        content={"message": "Unauthorized"}
                    )

        response = await call_next(request)
        return response


class AccessTokenCreator:
    def __init__(self, config: AuthConfig):
        self.secret_key = config.secret_key
        self.algorithm = config.algorithm

    def create_access_token(self, username: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        expire = datetime.now() + expires_delta
        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt
