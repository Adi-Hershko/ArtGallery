from app.exceptions import UserNotFoundException

# Dummy Data
fake_db = [
    {"username": "fakeuser", "password": "fakepass"},
    {"username": "fakeuser2", "password": "fakepass2"},
    {"username": "fakeuser3", "password": "fakepass3"}
]


def create_user(username: str, hashed_password: str) -> int:
    fake_db.append({"username": username, "password": hashed_password})
    return 1


# Create a class for custom expeptions
def get_hashed_password(username: str, password: str) -> str:
    for user in fake_db:
        if user["username"] == username:
            return user["password"]
    raise UserNotFoundException("User not found")

# Create a function that gets a password and returns a hashed password
