import pytest
from unittest.mock import patch
from app.schemas.book import Book as BookSchema
from app.core.exceptions import BookNotFoundError


@pytest.fixture
def mock_get(book_repository):
    with patch.object(book_repository, 'find_by_id') as mock:
        yield mock


def test_get_book_success(book_usecase, mock_get):
    book_id = 1
    expected_book = BookSchema(
        id=book_id,
        title="Test Book",
        author="Test Author",
        published_date="2023-01-01",
        isbn="1234567890123",
        pages=200
    )
    mock_get.return_value = expected_book

    result = book_usecase.get_book(book_id)

    assert result == expected_book
    mock_get.assert_called_once_with(book_id)


def test_get_book_not_found(book_usecase, mock_get):
    book_id = 999
    mock_get.return_value = None

    with pytest.raises(BookNotFoundError):
        book_usecase.get_book(book_id)

    mock_get.assert_called_once_with(book_id)
