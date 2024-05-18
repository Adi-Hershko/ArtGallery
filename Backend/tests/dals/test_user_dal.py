from unittest.mock import Mock
import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.DB.models import Base, User
from app.DB.db_operations import DatabaseOperations
from app.config.config import db_config
from app.dals.user_dal import UserDal
from app.exceptions import UserAlreadyExist


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
async def test_find_user_should_return_user(session: Session, db_teardown, db_operations):
    user = User(username='sample_username', password=b'sample_password', is_active=True)

    session.commit()
    session.add(user)
    session.commit()

    user_dal = UserDal(db_operations)
    fetched_user = await user_dal.find_user('sample_username')

    assert_user(user, fetched_user)


@pytest.mark.asyncio
async def test_find_user_should_return_none(session: Session, db_teardown, db_operations):
    user = User(username='sample_username', password=b'sample_password', is_active=True)

    session.commit()
    session.add(user)
    session.commit()

    user_dal = UserDal(db_operations)
    fetched_user = await user_dal.find_user('invalid_username')

    assert fetched_user is None


def assert_user(user: User, other_user: User):    
    assert user.username == other_user.username    
    assert user.password == other_user.password
  