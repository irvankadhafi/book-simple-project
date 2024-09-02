from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
from datetime import date
from cerberus import Validator
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, Book as BookSchema, BookSearchCriteria
from app.core.exceptions import BookNotFoundError, InvalidBookDataError


class BookUseCase:
    def __init__(self, repository: BookRepository):
        self.repository = repository
        self.validator = Validator({
            'title': {'type': 'string', 'minlength': 1, 'maxlength': 100},
            'author': {'type': 'string', 'minlength': 1, 'maxlength': 100},
            'published_date': {
                'type': 'date',
                'max': date.today(),
                'coerce': lambda s: date.fromisoformat(s) if isinstance(s, str) else s
            },
            'isbn': {
                'type': 'string',
                'regex': '^[0-9]{13}$'
            },
            'pages': {'type': 'integer', 'min': 1}
        })

    def validate_book_data(self, book: BookCreate):
        if not self.validator.validate(book.dict()):
            raise InvalidBookDataError(self.validator.errors)

    def create_book(self, book: BookCreate) -> BookSchema:
        self.validate_book_data(book)
        return self.repository.create(book)

    def get_book(self, book_id: int) -> BookSchema:
        book = self.repository.find_by_id(book_id)
        if not book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        return book

    def search_books(self, criteria: BookSearchCriteria) -> Tuple[List[BookSchema], int]:
        # Perform the search using the repository's search_by_page method

        # TODO: Consider optimizing the search functionality by implementing full-text search in PostgreSQL
        # or integrating Elasticsearch for better performance. The current ILIKE-based search might not
        # scale well with large datasets.

        book_ids, total = self.repository.search_by_page(criteria)

        # Fetch all books by IDs in parallel using ThreadPoolExecutor
        books = []

        # Use ThreadPoolExecutor to fetch books by ID in parallel
        with ThreadPoolExecutor() as executor:
            # Submit tasks for each book ID and map them to their futures
            future_to_id = {executor.submit(self.get_book, book_id): book_id for book_id in book_ids}

            # As each future completes, retrieve the result and store it in a dictionary
            books_map = {}
            for future in as_completed(future_to_id):
                book = future.result()
                if book:
                    books_map[future_to_id[future]] = book

        # Sort the books according to the original order of IDs
        for book_id in book_ids:
            if book_id in books_map:
                books.append(books_map[book_id])

        return books, total

    def update_book(self, book_id: int, book: BookCreate) -> BookSchema:
        self.validate_book_data(book)
        updated_book = self.repository.update(book_id, book)
        if not updated_book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        return updated_book

    def delete_book(self, book_id: int) -> bool:
        deleted = self.repository.delete(book_id)
        if not deleted:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        return True
