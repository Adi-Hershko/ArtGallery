from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, LargeBinary

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', password='{self.password}')>"
