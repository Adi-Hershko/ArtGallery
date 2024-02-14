from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Backend.app.config.models import DbConfig


class DatabaseOperations:
    def __init__(self, db_config: DbConfig):
        engine_url = (
            f'postgresql://{db_config.username}:{db_config.password}@'
            f'{db_config.host}:{db_config.port}/{db_config.database}'
        )

        self.engine = create_engine(engine_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
