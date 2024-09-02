import pytest
from app.models.book import Book as BookModel
from datetime import date


def test_delete_book_success(book_repository, clear_query_collector):
    # Create a book in the database
    book = BookModel(
        title="Test Book",
        author="Test Author",
        published_date=date(2023, 1, 1),
        isbn="1234567890",
        pages=200
    )
    book_repository.db.add(book)
    book_repository.db.commit()

    result = book_repository.delete(book.id)

    assert result is True
    db_book = book_repository.db.query(BookModel).filter(BookModel.id == book.id).first()
    assert db_book is not None
    assert db_book.deleted_at is not None  # Check that the book is soft-deleted


def test_delete_book_not_found(book_repository, clear_query_collector):
    book_id = 999

    result = book_repository.delete(book_id)

    assert result is False
