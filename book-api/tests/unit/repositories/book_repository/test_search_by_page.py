import pytest
from app.schemas.book import BookSearchCriteria
from app.models.book import Book as BookModel
from datetime import date


def test_search_by_page_success(book_repository, clear_query_collector):
    # Create some books in the database
    books = [
        BookModel(title="Book 1", author="Author 1", published_date=date(2023, 1, 1), isbn="1111111111", pages=100),
        BookModel(title="Book 2", author="Author 2", published_date=date(2023, 1, 2), isbn="2222222222", pages=200)
    ]
    book_repository.db.add_all(books)
    book_repository.db.commit()

    criteria = BookSearchCriteria(query="Book", page=1, size=10, sort=["created_at:desc"])
    book_ids, total = book_repository.search_by_page(criteria)

    assert len(book_ids) == 2
    assert total == 2
