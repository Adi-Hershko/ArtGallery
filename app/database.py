from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import UsersTable

# Setting up the database
engine = create_engine("postgresql://postgres:123456@localhost:5432/proj") # Change DB name later
Session = sessionmaker(bind=engine)
session = Session()

def create_record(data):
    new_record = UsersTable(**data)
    session.add(new_record)
    session.commit()

def get_all_records():
    return session.query(UsersTable).all()

def get_records_by_name(name):
    return session.query(UsersTable).filter(UsersTable.name == name).all()

def get_record_by_id(id):
    return session.query(UsersTable).filter(UsersTable.id == id).first()

def get_record_by_name(name):
    return session.query(UsersTable).filter(UsersTable.name == name).first()

def delete_record_by_id(id):
    session.query(UsersTable).filter(UsersTable.id == id).delete()
    session.commit()

def delete_record_by_name(name):
    session.query(UsersTable).filter(UsersTable.name == name).delete()
    session.commit()

def update_record_by_id(id, data):
    session.query(UsersTable).filter(UsersTable.id == id).update(data)
    session.commit()

def update_record_by_name(name, data):
    session.query(UsersTable).filter(UsersTable.name == name).update(data)
    session.commit()

# How to implement a db operation and close the connection afterwards
def some_db_operation():
    try:
        # Do something with the database
        pass
    except:
        # Handle exceptions
        pass
    finally:
        # Close the connection
        engine.dispose()
