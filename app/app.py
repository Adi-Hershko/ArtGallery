from fastapi import FastAPI
import bcrypt
from .database import *

app = FastAPI()

# Dummy Data
fake_db = [
    {"username": "fakeuser", "password": "fakepass"},
    {"username": "fakeuser2", "password": "fakepass2"},
    {"username": "fakeuser3", "password": "fakepass3"}
]

@app.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "Hello World"}

# Get all users - only for testing purposes
@app.get("/users", tags=["Users"])
async def get_users() -> dict:
    return {"users": fake_db}

# Sign up a new user    
@app.post("/sign-up", tags=["Users"])
async def sign_up(username:str, password:str) -> dict:
    # Hash the password
    salt = bcrypt.gensalt() # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    fake_db.append({"username": username, "password": hashed_password})
    return {"message": f"User {username} Created. Password: {password}"}

# Sign in a user
@app.post("/sign-in", tags=["Users"])
async def sign_in(username:str, password:str) -> dict:
    for user in fake_db:
        # Check if the username exists
        if user["username"] == username:
            # Check if the password matches
            if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                return {"message": f"{username} has been signed in."}
            else:
                return {"message": "Invalid Credentials"}
    return {"message": "User not found"}
