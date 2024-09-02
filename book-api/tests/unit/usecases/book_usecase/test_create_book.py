import pytest
from unittest.mock import patch
from datetime import date
from app.schemas.book import BookCreate, Book as BookSchema
from app.core.exceptions import InvalidBookDataError


@pytest.fixture
def mock_create(book_repository):
    with patch.object(book_repository, 'create') as mock:
        yield mock


def test_create_book_success(book_usecase, mock_create):
    book_data = BookCreate(
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )
    expected_book = BookSchema(id=1, **book_data.dict())
    mock_create.return_value = expected_book

    result = book_usecase.create_book(book_data)

    assert result == expected_book
    mock_create.assert_called_once_with(book_data)


def test_create_book_invalid_title(book_usecase):
    invalid_book_data = BookCreate(
        title="",  # Invalid: empty title
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.create_book(invalid_book_data)


def test_create_book_invalid_author(book_usecase):
    invalid_book_data = BookCreate(
        title="Valid Title",
        author="",  # Invalid: empty author
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.create_book(invalid_book_data)


def test_create_book_future_date(book_usecase):
    future_book_data = BookCreate(
        title="Future Book",
        author="Test Author",
        published_date=date(2025, 1, 1),  # Future date
        isbn="1234567890123",
        pages=200
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.create_book(future_book_data)


def test_create_book_invalid_isbn(book_usecase):
    invalid_isbn_data = BookCreate(
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="12345",  # Invalid ISBN
        pages=200
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.create_book(invalid_isbn_data)


def test_create_book_invalid_pages(book_usecase):
    invalid_pages_data = BookCreate(
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=0  # Invalid pages
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.create_book(invalid_pages_data)
