from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User
from .db_setup import login_info # remove later

# Database operations class
class DatabaseOperations:
    def __init__(self):
        engine_url = f'postgresql://{login_info["username"]}:{login_info["password"]}@{login_info["host"]}:{login_info["port"]}/{login_info["db_name"]}'
        self.engine = create_engine(engine_url)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, username, password):
        session = self.Session()
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
        session.close()
        print(f"User '{username}' added successfully.")

    def find_user(self, username):
        session = self.Session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        return user

    def delete_user(self, username):
        session = self.Session()
        user = session.query(User).filter(User.username == username).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"User '{username}' deleted successfully.")
        else:
            print(f"User '{username}' not found.")
        session.close()

# Example usage
if __name__ == "__main__":
    db_ops = DatabaseOperations('your_username', 'your_password', 'localhost', '5432', 'ArtGallery')

    # Add a user
    db_ops.add_user('johndoe', 'password123')

    # Find a user
    user = db_ops.find_user('johndoe')
    if user:
        print(f"User found: {user.username}")

    # Delete a user
    db_ops.delete_user('johndoe')
