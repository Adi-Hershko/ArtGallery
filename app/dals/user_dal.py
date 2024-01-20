from app.exceptions import UserNotFoundException
from app.DB.db_operations import DatabaseOperations
from kink import inject
from ..DB.models import User

@inject
async def add_user(username, password, db_operations: DatabaseOperations) -> int:
        print("Insterting user...")
        try:
            async with db_operations.get_session() as session:
                print("Adding user...")
                new_user = User(username=username, password=password)
                print("New user: ", new_user)            
                session.add(new_user)
                print("User added.")
                await session.commit()

            print(f"User '{username}' added successfully.")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0

def find_user(self, username):
    pass
    # session = self.Session()
    # user = session.query(User).filter(User.username == username).first()
    # session.close()
    # return user


def delete_user(self, username):
    pass
    # session = self.Session()
    # user = session.query(User).filter(User.username == username).first()
    # if user:
    #     session.delete(user)
    #     session.commit()
    #     print(f"User '{username}' deleted successfully.")
    # else:
    #     print(f"User '{username}' not found.")
    # session.close()