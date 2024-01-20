from kink import di
from app.DB.db_operations import DatabaseOperations

di[DatabaseOperations] = DatabaseOperations()