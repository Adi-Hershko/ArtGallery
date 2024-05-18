from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

from app.DB.models import Base, User
from app.DB.db_operations import DatabaseOperations
from app.DB.models import Post
from app.dals.post_dal import PostDal
from app.config.config import db_config


@pytest.fixture(autouse=True)
def session():
    engine = create_engine(
        f'postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}'
    )

    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


@pytest.fixture(autouse=True)
def db_teardown(request):
    engine = create_engine(
        f'postgresql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}'
    )

    def teardown():
        metadata = MetaData()
        metadata.reflect(bind=engine)

        for tbl in reversed(metadata.sorted_tables):
            tbl.drop(engine)

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def db_operations(session) -> DatabaseOperations:
    db_operation = DatabaseOperations
    db_operation.get_session = Mock()
    db_operation.get_session.return_value = session

    return db_operation


@pytest.mark.asyncio
async def test_post(session: Session, db_teardown, db_operations):
    post = Post(
        username='sample_username',
        title='Sample Title',
        description='Sample Description',
        path_to_image='/path/to/image.jpg',
        is_active=True)

    session.add(User(
        username="sample_username",
        password=b"test",
        is_active=False
    ))

    session.commit()
    session.add(post)
    session.commit()

    post_dal = PostDal(db_operations)
    result_posts = await post_dal.get_all_posts({})

    assert len(result_posts) == 1
    assert_post(post, result_posts[0])


def assert_post(post: Post, other: Post):
    assert post.username == other.username
    assert post.title == other.title    
    assert post.insertion_time == other.insertion_time
    assert post.description == other.description
    assert post.is_active == other.is_active
    assert post.path_to_image == other.path_to_image
