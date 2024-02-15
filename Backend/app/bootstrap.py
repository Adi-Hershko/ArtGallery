from botocore.client import BaseClient
from kink import di
from Backend.app.config.config import db_config
from Backend.app.DB.db_operations import DatabaseOperations
from Backend.app.object_storage.os_helper import get_s3_client


def bootstrap_di() -> None:
    di[DatabaseOperations] = DatabaseOperations(db_config)
    di[BaseClient] = get_s3_client()
