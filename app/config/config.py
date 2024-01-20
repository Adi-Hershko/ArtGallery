from dotenv import load_dotenv
import os
from .models import DbConfig

load_dotenv()

db_config = DbConfig(
    username = os.getenv("DB_USERNAME"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    database = os.getenv("DB_NAME")
)