from dotenv import load_dotenv
from Backend.app.config.models import DbConfig
import os

load_dotenv()

db_config = DbConfig(
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

env = os.getenv("ENV", "dev")
origins = os.getenv("ORIGINS", ["*"] if env == "dev" else [])
