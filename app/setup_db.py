from sqlalchemy import create_engine
from .models import Base

def create_database():
    engine = create_engine("postgresql://postgres:123456@localhost:5432/proj") # Change DB name later
    Base.metadata.create_all(engine)

# The if __name__ == "__main__": block ensures that this code is executed when you run setup_db.py
# To create the database, run python setup_db.py in the terminal
if __name__ == "__main__":
    create_database()
    print("Database tables created successfully.")
