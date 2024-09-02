import pytest
from unittest.mock import patch
from datetime import date
from app.schemas.book import BookCreate, Book as BookSchema
from app.core.exceptions import BookNotFoundError, InvalidBookDataError


@pytest.fixture
def mock_update(book_repository):
    with patch.object(book_repository, 'update') as mock:
        yield mock


def test_update_book_success(book_usecase, mock_update):
    book_id = 1
    update_data = BookCreate(
        title="Updated Book",
        author="Updated Author",
        published_date=date(2023, 2, 1),
        isbn="9876543210123",
        pages=250
    )
    expected_book = BookSchema(id=book_id, **update_data.dict())
    mock_update.return_value = expected_book

    result = book_usecase.update_book(book_id, update_data)

    assert result == expected_book
    mock_update.assert_called_once_with(book_id, update_data)


def test_update_book_not_found(book_usecase, mock_update):
    book_id = 999
    update_data = BookCreate(
        title="Updated Book",
        author="Updated Author",
        published_date=date(2023, 2, 1),
        isbn="9876543210123",
        pages=250
    )
    mock_update.return_value = None

    with pytest.raises(BookNotFoundError):
        book_usecase.update_book(book_id, update_data)

    mock_update.assert_called_once_with(book_id, update_data)


def test_update_book_invalid_data(book_usecase):
    book_id = 1
    invalid_update_data = BookCreate(
        title="",  # Invalid: empty title
        author="Updated Author",
        published_date=date(2023, 2, 1),
        isbn="9876543210123",
        pages=250
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.update_book(book_id, invalid_update_data)


def test_update_book_future_date(book_usecase):
    book_id = 1
    future_update_data = BookCreate(
        title="Updated Book",
        author="Updated Author",
        published_date=date(2025, 1, 1),  # Future date
        isbn="9876543210123",
        pages=250
    )

    with pytest.raises(InvalidBookDataError):
        book_usecase.update_book(book_id, future_update_data)
