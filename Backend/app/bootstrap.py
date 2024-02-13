from kink import di
from app.DB.db_operations import DatabaseOperations
from app.config.config import db_config


def bootstrap_di() -> None:
    di[DatabaseOperations] = DatabaseOperations(db_config)
