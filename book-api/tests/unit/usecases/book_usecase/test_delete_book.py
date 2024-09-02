import pytest
from unittest.mock import patch
from app.core.exceptions import BookNotFoundError


@pytest.fixture
def mock_delete(book_repository):
    with patch.object(book_repository, 'delete') as mock:
        yield mock


def test_delete_book_success(book_usecase, mock_delete):
    book_id = 1
    mock_delete.return_value = True

    result = book_usecase.delete_book(book_id)

    assert result is True
    mock_delete.assert_called_once_with(book_id)


def test_delete_book_not_found(book_usecase, mock_delete):
    book_id = 999
    mock_delete.return_value = False

    with pytest.raises(BookNotFoundError):
        book_usecase.delete_book(book_id)

    mock_delete.assert_called_once_with(book_id)
