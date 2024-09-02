import pytest
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.book import BookCreate, Book as BookSchema
from app.models.book import Book as BookModel

def test_update_book_success(book_repository, clear_query_collector):
    # Create a book in the database
    book = BookModel(
        title="Old Title",
        author="Old Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890123",
        pages=200
    )
    book_repository.db.add(book)
    book_repository.db.commit()

    update_data = BookCreate(
        title="Updated Book",
        author="Updated Author",
        published_date=date(2023, 2, 1),
        isbn="9876543210123",
        pages=250
    )

    result = book_repository.update(book.id, update_data)

    assert isinstance(result, BookSchema)
    assert result.id == book.id
    assert result.title == "Updated Book"
    assert result.author == "Updated Author"

def test_update_book_not_found(book_repository, clear_query_collector):
    book_id = 999
    update_data = BookCreate(
        title="Updated Book",
        author="Updated Author",
        published_date=date(2023, 2, 1),
        isbn="9876543210123",
        pages=250
    )

    result = book_repository.update(book_id, update_data)

    assert result is None
