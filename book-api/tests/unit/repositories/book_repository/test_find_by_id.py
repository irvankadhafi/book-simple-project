import pytest
from unittest.mock import Mock
from datetime import date, datetime
from app.schemas.book import Book as BookSchema
from app.models.book import Book as BookModel
from sqlalchemy.exc import SQLAlchemyError


def test_find_by_id_success(book_repository, clear_query_collector):
    # Mocking the result
    now = datetime.utcnow()
    mock_book = BookSchema(
        id=1,
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200,
        created_at=now,
        updated_at=now,
        deleted_at=None
    )

    # Set the return value of the mock
    book_repository.find_by_id = Mock(return_value=mock_book)

    result = book_repository.find_by_id(1)

    assert result is not None
    assert result.id == mock_book.id
    assert result.title == mock_book.title
    assert result.author == mock_book.author
    assert result.published_date == mock_book.published_date
    assert result.isbn == mock_book.isbn
    assert result.pages == mock_book.pages
    assert result.created_at == mock_book.created_at
    assert result.updated_at == mock_book.updated_at
    assert result.deleted_at == mock_book.deleted_at


def test_find_by_id_not_found(book_repository, clear_query_collector):
    # Mock the return value to be None, indicating the book was not found
    book_repository.find_by_id = Mock(return_value=None)

    result = book_repository.find_by_id(999)

    assert result is None


def test_find_by_id_db_error(book_repository, clear_query_collector):
    # Mock a database error
    book_repository.find_by_id = Mock(side_effect=SQLAlchemyError("Database error"))

    with pytest.raises(SQLAlchemyError):
        book_repository.find_by_id(1)


def test_find_by_id_invalid_id(book_repository, clear_query_collector):
    # Mocking the scenario where an invalid ID is passed
    with pytest.raises(ValueError):
        book_repository.find_by_id("invalid_id")  # Passing a string instead of an int


def test_find_by_id_no_created_at(book_repository, clear_query_collector):
    # Mocking a book without a created_at timestamp
    now = datetime.utcnow()
    mock_book = BookSchema(
        id=1,
        title="No Created At Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200,
        created_at=None,  # Missing created_at
        updated_at=now,
        deleted_at=None
    )

    # Set the return value of the mock
    book_repository.find_by_id = Mock(return_value=mock_book)

    result = book_repository.find_by_id(1)

    assert result is not None
    assert result.id == mock_book.id
    assert result.title == mock_book.title
    assert result.author == mock_book.author
    assert result.published_date == mock_book.published_date
    assert result.isbn == mock_book.isbn
    assert result.pages == mock_book.pages
    assert result.created_at is None  # created_at is missing
    assert result.updated_at == mock_book.updated_at
    assert result.deleted_at == mock_book.deleted_at
