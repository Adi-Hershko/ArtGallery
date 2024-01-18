from .database import create_record, get_records_by_name

# Example of a function that uses the database
def add_new_record(name):
    data = {'name': name}
    create_record(data)

def search_records(name):
    return get_records_by_name(name)

