import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.book import BookCreate, Book as BookSchema
from app.core.exceptions import InvalidBookDataError
from unittest.mock import patch
from datetime import date

client = TestClient(app)


@pytest.fixture
def mock_create_book():
    with patch("app.usecases.book_usecase.BookUseCase.create_book") as mock:
        yield mock


def test_create_book_success(mock_create_book):
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "isbn": "1234567890123",
        "pages": 200
    }
    expected_book = BookSchema(id=1, **book_data)
    mock_create_book.return_value = expected_book

    response = client.post("/api/v1/books/", json=book_data)

    assert response.status_code == 201
    assert response.json()["data"]["id"] == expected_book.id
    mock_create_book.assert_called_once()


def test_create_book_invalid_data(mock_create_book):
    book_data = {
        "title": "",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "isbn": "1234567890123",
        "pages": 200
    }
    # Change from ValueError to InvalidBookDataError
    mock_create_book.side_effect = InvalidBookDataError("Invalid book data provided.")

    response = client.post("/api/v1/books/", json=book_data)

    assert response.status_code == 400
    assert response.json()["errors"]["message"] == "Invalid book data provided."
    mock_create_book.assert_called_once()
