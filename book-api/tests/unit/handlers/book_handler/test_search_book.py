import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.book import BookSearchCriteria, Book as BookSchema
from unittest.mock import patch
from datetime import date, datetime

client = TestClient(app)


@pytest.fixture
def mock_search_books():
    with patch("app.usecases.book_usecase.BookUseCase.search_books") as mock:
        yield mock


def test_search_books_success(mock_search_books):
    search_criteria = BookSearchCriteria(query="Test", page=1, size=10, sort=["created_at:desc"])
    expected_books = [
        BookSchema(
            id=1,
            title="Test Book 1",
            author="Test Author 1",
            published_date=date(2023, 1, 1),
            isbn="1234567890123",
            pages=200,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None
        ),
        BookSchema(
            id=2,
            title="Test Book 2",
            author="Test Author 2",
            published_date=date(2023, 1, 2),
            isbn="1234567890124",
            pages=250,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None
        )
    ]
    mock_search_books.return_value = (expected_books, len(expected_books))

    response = client.get("/api/v1/books/", params={"query": "Test", "page": 1, "size": 10})

    assert response.status_code == 200
    assert len(response.json()["data"]["items"]) == len(expected_books)
    mock_search_books.assert_called_once()


def test_search_books_invalid_criteria():
    response = client.get("/api/v1/books/", params={"page": 0, "size": 25})

    assert response.status_code == 422
    assert "value is greater than or equal to 1" in response.json()["detail"][0]["msg"]
    assert "value is less than or equal to 20" in response.json()["detail"][1]["msg"]
