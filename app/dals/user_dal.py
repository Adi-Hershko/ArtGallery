from app.exceptions import UserNotFoundException
from app.DB.db_operations import DatabaseOperations
from ..DB.models import User

async def add_user(username, password) -> int:
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
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0

async def find_user(username):
    print("Finding user...")
    try:
        db_operations = DatabaseOperations()
        with db_operations.get_session() as session:
            print("locating user...")
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return UserNotFoundException(f"User '{username}' not found.")            
            print("User found: ", user)
            return user
    except Exception as e:
        print(f"Error: {e}")
        # Maybe return a DB exception here
        return None
        


def delete_user(self, username):
    pass
    