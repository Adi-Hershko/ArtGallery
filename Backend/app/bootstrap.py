from kink import di
from Backend.app.config.config import db_config
from Backend.app.DB.db_operations import DatabaseOperations


def bootstrap_di() -> None:
    di[DatabaseOperations] = DatabaseOperations(db_config)
