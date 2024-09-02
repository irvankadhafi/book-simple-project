import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.db.postgresql import Base
from app.repositories.book_repository import BookRepository
from app.usecases import BookUseCase
from unittest.mock import Mock
from tests.utils import query_collector


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        query_collector.collect(statement)

    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def book_repository(db_session):
    mock_cache = Mock()
    return BookRepository(db=db_session, cache=mock_cache)


@pytest.fixture
def book_usecase(book_repository):
    return BookUseCase(book_repository)


@pytest.fixture(autouse=True)
def clear_query_collector():
    query_collector.clear()
    yield
    query_collector.print_queries()
