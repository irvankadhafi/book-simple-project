import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import BookNotFoundError
from unittest.mock import patch

client = TestClient(app)


@pytest.fixture
def mock_delete_book():
    with patch("app.usecases.book_usecase.BookUseCase.delete_book") as mock:
        yield mock


def test_delete_book_success(mock_delete_book):
    book_id = 1
    mock_delete_book.return_value = True

    response = client.delete(f"/api/v1/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["data"] == {}
    mock_delete_book.assert_called_once_with(book_id)


def test_delete_book_not_found(mock_delete_book):
    book_id = 999
    mock_delete_book.side_effect = BookNotFoundError("Book not found.")

    response = client.delete(f"/api/v1/books/{book_id}")

    assert response.status_code == 404
    assert response.json()["errors"]["message"] == "Book not found."
    mock_delete_book.assert_called_once_with(book_id)
