import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from app.schemas.book import BookCreate, Book as BookSchema
from app.models.book import Book as BookModel

def test_create_book_success(book_repository, clear_query_collector):
    book_data = BookCreate(
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )

    result = book_repository.create(book_data)

    assert isinstance(result, BookSchema)
    assert result.id is not None
    assert result.title == "Test Book"
    assert result.author == "Test Author"

    # Verify book is in the database
    db_book = book_repository.db.query(BookModel).filter(BookModel.id == result.id).first()
    assert db_book is not None
    assert db_book.title == "Test Book"

def test_create_book_duplicate_isbn(book_repository, clear_query_collector):
    book_data1 = BookCreate(
        title="Book 1",
        author="Author 1",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )
    book_repository.create(book_data1)

    book_data2 = BookCreate(
        title="Book 2",
        author="Author 2",
        published_date=date(2023, 1, 2),
        isbn="1234567890123",  # Same ISBN
        pages=250
    )

    with pytest.raises(IntegrityError):
        book_repository.create(book_data2)
