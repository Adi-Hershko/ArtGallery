import psycopg2
from sqlalchemy import create_engine, exc
from sqlalchemy_utils import database_exists, create_database
from DB.models import Base
from config import db_config

def create_database_and_tables(username, password, host, port, db_name):
    # Connection string
    db_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'

    # Create the database if it doesn't exist
    if not database_exists(db_url):
        try:
            create_database(db_url)
            print(f"Database '{db_name}' created successfully.") # change to log later
        except exc.SQLAlchemyError as e:
            print(f"An error occurred while creating the database: {e}")
            return

    # Connect to the database and create tables
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except exc.SQLAlchemyError as e:
        print(f"An error occurred while creating the tables: {e}")

# Directly runnable for testing
if __name__ == "__main__":
    create_database_and_tables(db_config.username, db_config.password, db_config.host, db_config.port, db_config.database)