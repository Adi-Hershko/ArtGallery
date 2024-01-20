from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User
from ..config import db_config


# Database operations class
class DatabaseOperations:
    def __init__(self):
        engine_url = f'postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{int(db_config.port)}/{db_config.database}'
        self.engine = create_engine(engine_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()