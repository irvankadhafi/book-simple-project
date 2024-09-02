import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.book import BookCreate, Book as BookSchema
from app.core.exceptions import BookNotFoundError, InvalidBookDataError
from unittest.mock import patch
from datetime import date, datetime

client = TestClient(app)


@pytest.fixture
def mock_update_book():
    with patch("app.usecases.book_usecase.BookUseCase.update_book") as mock:
        yield mock


def test_update_book_success(mock_update_book):
    book_id = 1
    update_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_date": "2023-02-01",
        "isbn": "9876543210123",
        "pages": 250
    }
    expected_book = BookSchema(id=book_id, **update_data, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None)
    mock_update_book.return_value = expected_book

    response = client.put(f"/api/v1/books/{book_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["data"]["id"] == expected_book.id
    mock_update_book.assert_called_once_with(book_id, BookCreate(**update_data))


def test_update_book_not_found(mock_update_book):
    book_id = 999
    update_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_date": "2023-02-01",
        "isbn": "9876543210123",
        "pages": 250
    }
    mock_update_book.side_effect = BookNotFoundError("Book not found.")

    response = client.put(f"/api/v1/books/{book_id}", json=update_data)

    assert response.status_code == 404
    assert response.json()["errors"]["message"] == "Book not found."
    mock_update_book.assert_called_once_with(book_id, BookCreate(**update_data))


def test_update_book_invalid_data(mock_update_book):
    book_id = 1
    update_data = {
        "title": "",
        "author": "Updated Author",
        "published_date": "2023-02-01",
        "isbn": "9876543210123",
        "pages": 250
    }
    mock_update_book.side_effect = InvalidBookDataError("Invalid book data provided.")

    response = client.put(f"/api/v1/books/{book_id}", json=update_data)

    assert response.status_code == 400
    assert response.json()["errors"]["message"] == "Invalid book data provided."
    mock_update_book.assert_called_once_with(book_id, BookCreate(**update_data))
