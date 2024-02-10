from kink import di
import inspect
from app.exceptions import OperationError, UserAlreadyExist
from app.DB.db_operations import DatabaseOperations
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.DB.models import User

db_operations = di[DatabaseOperations]


async def add_user(user: User) -> None:
    print("Inserting user...")
    with db_operations.get_session() as session:
        print("Adding user...")
        print("New user: ", user)
        session.add(user)
        try:
            session.commit()
            print("User added.")
        except IntegrityError as exc:
            if isinstance(exc.orig, UniqueViolation):
                print(f"Error: User with username '{user.username}' already exists.")
                raise UserAlreadyExist("User already exists.")
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            print(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")


async def find_user(username: str) -> User:
    print("Finding user...")
    with db_operations.get_session() as session:
        print("Locating user...")
        try:
            query_result = session.query(User).filter(User.username == username).first()
            print("User found: ", query_result) if query_result else print("User not found.")
            return User(username=query_result.username, password=query_result.password) if query_result else None            
        except Exception as e:
            module_name = __name__
            function_name = inspect.currentframe().f_code.co_name
            print(f"Error in {module_name}.{function_name}: Error: {e}")
            raise OperationError("Operation error.")