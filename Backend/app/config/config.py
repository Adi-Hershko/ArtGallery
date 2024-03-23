from dotenv import load_dotenv
from app.config.models import DbConfig, S3Config, AuthConfig
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
origins = os.getenv("ORIGINS", ["http://localhost:5173"] if env == "dev" else [])

s3_config = S3Config(
    os.getenv("AWS_ACCESS_KEY"),
    os.getenv("AWS_SECRET_ACCESS_KEY"),
    os.getenv("BUCKET_NAME")
)

if env == 'dev':
    s3_config.endpoint_url = os.getenv("S3_LOCAL_URL")

THUMBNAILS_SIZE = (100, 100)

auth_config = AuthConfig(
        secret_key=os.getenv("AUTH_SECRET_KEY", "dev"),
        algo=os.getenv("AUTH_ALGORITH", "HS256")
)

