from typing import Optional

from kink import inject
from app.exceptions import OperationError, UserAlreadyExist
from app.DB.db_operations import DatabaseOperations
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.DB.models import User
from app import logger

module_name = __name__


@inject
class UserDal:
    def __init__(self, db_operations: DatabaseOperations):
        self.db_operations = db_operations

    async def add_user(self, user: User) -> None:
        logger.info(f"{module_name}.add_user Inserting user {user.username}")
        with self.db_operations.get_session() as session:
            session.add(user)
            try:
                session.commit()
            except IntegrityError as exc:
                if isinstance(exc.orig, UniqueViolation):
                    logger.error(f"{module_name}.add_user Error: User with username '{user.username}' already exists.")
                    raise UserAlreadyExist("User already exists.")
            except Exception as e:
                logger.error(f"{module_name}.add_user Failed adding user, Error: {e}")
                raise OperationError("Operation error.")
            else:
                logger.info(f"{module_name}.add_user User added.")

    async def find_user(self, username: str) -> Optional[User]:
        logger.info(f"{module_name}.find_user Finding user {username}")
        with self.db_operations.get_session() as session:
            try:
                query_result = session.query(User).filter(User.username == username).first()
            except OperationError as e:
                logger.error(f"{module_name}.find_user Error: {e}")
                raise OperationError("Operation error.")
            else:
                if query_result:
                    logger.info(f"{module_name}.find_user User found {username}")
                    return User(username=query_result.username, password=query_result.password)
                else:
                    logger.info(f"{module_name}.find_user User not found with username {username}.")
                    return None
