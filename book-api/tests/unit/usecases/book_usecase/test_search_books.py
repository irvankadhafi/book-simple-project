import pytest
from unittest.mock import patch
from app.schemas.book import Book as BookSchema
from app.schemas.book import BookSearchCriteria


@pytest.fixture
def mock_search_by_page(book_repository):
    with patch.object(book_repository, 'search_by_page') as mock:
        yield mock


@pytest.fixture
def mock_get(book_usecase):
    with patch.object(book_usecase, 'get_book') as mock:
        yield mock


def test_search_books_success(book_usecase, mock_search_by_page, mock_get):
    criteria = BookSearchCriteria(query="Test", page=1, size=10)
    mock_search_by_page.return_value = ([1, 2], 2)

    mock_get.side_effect = [
        BookSchema(id=1, title="Book 1", author="Author 1", published_date="2023-01-01", isbn="1234567890123",
                   pages=200),
        BookSchema(id=2, title="Book 2", author="Author 2", published_date="2023-02-01", isbn="2345678901234",
                   pages=300),
    ]

    books, total = book_usecase.search_books(criteria)

    assert total == 2
    assert len(books) == 2
    assert books[0].id == 1
    assert books[1].id == 2
    mock_search_by_page.assert_called_once_with(criteria)


def test_search_books_empty(book_usecase, mock_search_by_page):
    criteria = BookSearchCriteria(query="Nonexistent", page=1, size=10)
    mock_search_by_page.return_value = ([], 0)

    books, total = book_usecase.search_books(criteria)

    assert total == 0
    assert len(books) == 0
    mock_search_by_page.assert_called_once_with(criteria)
