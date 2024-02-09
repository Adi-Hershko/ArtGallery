from ..exceptions import OperationError, UserAlreadyExist
from kink import di

from app.DB.db_operations import DatabaseOperations
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from ..DB.models import User
from ..pydantic_models.user_models.user_request_model import UserBaseRequestModel, UserInternalRequestModel
from ..pydantic_models.user_models.user_response_model import UserBaseResponseModel, UserInternalResponseModel

db_operations = di[DatabaseOperations]


async def add_user(username, password) -> int:
    print("Inserting user...")
    try:
        with db_operations.get_session() as session:
            print("Adding user...")
            new_user = User(username=username, password=password, is_active=True)
            print("New user: ", new_user)
            session.add(new_user)
            print("User added.")
            session.commit()
            session.close()

        print(f"User '{username}' added successfully.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 0
async def add_user(user: UserInternalRequestModel) -> None:
        print("Inserting user...")
        try:
            db_operations = DatabaseOperations()
            with db_operations.get_session() as session:
                print("Adding user...")
                new_user = User(username=user.username, password=user.password, is_active=True)
                print("New user: ", new_user)            
                session.add(new_user)
                session.commit()
                print("User added.")
                session.close()
            print(f"User '{user.username}' added successfully.")
        except IntegrityError as exc:
            if isinstance(exc.orig, UniqueViolation):
                print(f"Error: User with username '{user.username}' already exists.")
                raise UserAlreadyExist("User already exists.")
        except Exception as e:
            print(f"Error: {e}")
            raise OperationError("Error creating user.")

async def find_user(user: UserBaseRequestModel) -> UserInternalResponseModel:

async def find_user(username):
    print("Finding user...")
    try:
        with db_operations.get_session() as session:
            print("Locating user...")
            query_result = session.query(User).filter(User.username == user.username).first()
            print("User found: ", query_result) if query_result else print("User not found.")
            session.close()
            return UserInternalResponseModel(username=query_result.username, password=query_result.password) if query_result else None
    except Exception as e:
        print(f"Error: {e}")
        return None

        print(f"Error: {e}")        
        raise OperationError("Error finding user.")