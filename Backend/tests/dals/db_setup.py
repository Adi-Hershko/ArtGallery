from sqlalchemy import create_engine, exc, inspect
from sqlalchemy_utils import database_exists, create_database
from app.DB.models import Base
from app.config.config import db_config
from app.application import logger
from tests.dals import db_config


def create_database_and_tables(username, password, host, port, db_name):
    db_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'

    if not database_exists(db_url):
        try:
            create_database(db_url)
            logger.info(f"Database '{db_name}' created successfully.")  # change to log later
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while creating the database: {e}")
            return

    try:
        engine = create_engine(db_url)
    except exc.SQLAlchemyError as e:
        print(f"An error occurred while connecting to the database: {e}")
        return

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if not set(Base.metadata.tables.keys()).issubset(set(tables)):
        try:
            Base.metadata.create_all(engine)
            logger.info("Tables created successfully.")
        except exc.SQLAlchemyError as e:
            logger.error(f"An error occurred while creating the tables: {e}")


def create_db():
    create_database_and_tables(env.DB_NAME, env.DB_PASSWORD, env.DB_HOST, env.DB_PORT, env.DB_NAME)

