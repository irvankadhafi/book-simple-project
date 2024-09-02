import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.book import Book as BookSchema
from app.core.exceptions import BookNotFoundError
from unittest.mock import patch
from datetime import date, datetime

client = TestClient(app)


@pytest.fixture
def mock_get_book():
    with patch("app.usecases.book_usecase.BookUseCase.get_book") as mock:
        yield mock


def test_read_book_success(mock_get_book):
    book_id = 1
    expected_book = BookSchema(
        id=book_id,
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None
    )
    mock_get_book.return_value = expected_book

    response = client.get(f"/api/v1/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == expected_book.id
    mock_get_book.assert_called_once_with(book_id)


def test_read_book_not_found(mock_get_book):
    book_id = 999
    mock_get_book.side_effect = BookNotFoundError("Book not found.")

    response = client.get(f"/api/v1/books/{book_id}")

    assert response.status_code == 404
    assert response.json()["errors"]["message"] == "Book not found."
    mock_get_book.assert_called_once_with(book_id)
