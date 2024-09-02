from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from app.models.book import Book
from app.schemas.book import BookCreate, Book as BookSchema, BookSearchCriteria, parse_sort_param
from app.cacher.cache_manager import CacheManager, find_from_cache_by_key
from datetime import datetime
import json

ALLOWED_SORT_FIELDS = {
    'title': Book.title,
    'author': Book.author,
    'published_date': Book.published_date,
    'pages': Book.pages,
    'created_at': Book.created_at,
    'updated_at': Book.updated_at
}


def new_cache_key_by_id(book_id: int) -> str:
    return f"cache:object:book:id:{book_id}"


class BookRepository:
    def __init__(self, db: Session, cache: CacheManager):
        self.db = db
        self.cache = cache

    def find_by_id(self, book_id: int) -> BookSchema:
        cache_key = new_cache_key_by_id(book_id)
        cached_book = find_from_cache_by_key(self.cache, cache_key)
        if cached_book:
            return BookSchema.parse_raw(cached_book)

        # Ensure soft-delete is respected
        book = self.db.query(Book).filter(Book.id == book_id, Book.deleted_at.is_(None)).first()
        if book:
            book_schema = BookSchema.from_orm(book)
            self.cache.set(cache_key, book_schema.json())
            return book_schema
        return None

    def create(self, book: BookCreate) -> BookSchema:
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        self.delete_caches(db_book)
        return BookSchema.from_orm(db_book)

    def update(self, book_id: int, book: BookCreate) -> BookSchema:
        # Soft-delete filter
        db_book = self.db.query(Book).filter(Book.id == book_id, Book.deleted_at.is_(None)).first()
        if db_book:
            for key, value in book.dict().items():
                setattr(db_book, key, value)
            db_book.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_book)
            self.delete_caches(db_book)
            return BookSchema.from_orm(db_book)
        return None

    def delete(self, book_id: int) -> bool:
        db_book = self.db.query(Book).filter(Book.id == book_id, Book.deleted_at.is_(None)).first()
        if db_book:
            # Perform soft delete
            db_book.deleted_at = datetime.utcnow()
            self.db.commit()
            self.delete_caches(db_book)
            return True
        return False

    def search_by_page(self, criteria: BookSearchCriteria):
        criteria.set_default_value()
        # Soft-delete filter
        base_query = self.db.query(Book.id).filter(Book.deleted_at.is_(None))
        if criteria.query:
            # Concatenate the fields 'title', 'author', and 'isbn' into a single string
            concatenated_fields = func.concat_ws(' ', Book.title, Book.author, Book.isbn)

            # Apply an ILIKE filter on the concatenated string to match the search query
            base_query = base_query.filter(concatenated_fields.ilike(f"%{criteria.query}%"))

        total = base_query.count()

        for sort_param in criteria.sort:
            field, direction = parse_sort_param(sort_param)
            if field in ALLOWED_SORT_FIELDS:
                order_func = desc if direction == 'DESC' else asc
                base_query = base_query.order_by(order_func(ALLOWED_SORT_FIELDS[field]))

        book_ids = base_query.offset((criteria.page - 1) * criteria.size).limit(criteria.size).all()
        book_ids = [book_id[0] for book_id in book_ids]  # Extract IDs from tuples

        return book_ids, total

    def delete_caches(self, book: Book):
        self.cache.delete(new_cache_key_by_id(book.id))
