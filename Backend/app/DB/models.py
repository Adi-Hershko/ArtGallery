from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, LargeBinary, UUID, DateTime, ForeignKey, func
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', password='{self.password}')>"


class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    path_to_image = Column(String, nullable=False)
    path_to_thumbnail = Column(String, nullable=False)
    insertion_time = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return (
            f"<Post(post_id='{self.post_id}',"
            f" username='{self.username}',"
            f" title='{self.title}',"
            f" description='{self.description}',"
            f" path_to_image='{self.path_to_image}',"
            f" path_to_thumbnail='{self.path_to_thumbnail}',"
            f"  insertion_time='{self.insertion_time}',"
            f" is_active='{self.is_active}')>"
        )
