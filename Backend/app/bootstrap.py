from botocore.client import BaseClient
from kink import di
from app.config.config import db_config, auth_config
from app.DB.db_operations import DatabaseOperations
from app.dals.post_dal import PostDal
from app.dals.user_dal import UserDal
from app.object_storage.os_helper import get_s3_client
from app.routes.middlewares.auth_middleware import AccessTokenCreator
from app.services.post_service import PostService
from app.services.user_service import UserService


def bootstrap_di() -> None:
    di[DatabaseOperations] = DatabaseOperations(db_config)
    di[BaseClient] = get_s3_client()
    di[PostDal] = PostDal()
    di[UserDal] = UserDal()
    di[PostService] = PostService()
    di[UserService] = UserService()
    di[AccessTokenCreator] = AccessTokenCreator(auth_config)
