from ..exceptions import OperationError
from app.DB.db_operations import DatabaseOperations
from ..DB.models import User

async def add_user(username, password):
        print("Inserting user...")
        try:
            db_operations = DatabaseOperations()
            with db_operations.get_session() as session:
                print("Adding user...")
                new_user = User(username=username, password=password, is_active=True)
                print("New user: ", new_user)            
                session.add(new_user)
                print("User added.")
                session.commit()
                session.close()
            print(f"User '{username}' added successfully.")            
        except Exception as e:
            print(f"Error: {e}")
            raise OperationError("Error creating user.")

async def find_user(username) -> User:
    print("Finding user...")
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("Locating user...")
            user = session.query(User).filter(User.username == username).first()
            print("User found: ", user) if user else print("User not found.")
            session.close()
            return user
    except Exception as e:
        print(f"Error: {e}")        
        raise OperationError("Error finding user.")