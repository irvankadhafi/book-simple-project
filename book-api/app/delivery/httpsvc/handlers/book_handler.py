from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from app.schemas.book import BookCreate, Book as BookSchema, BookSearchCriteria
from app.usecases.book_usecase import BookUseCase
from app.repositories.book_repository import BookRepository
from app.core.exceptions import BookNotFoundError, InvalidBookDataError
from app.cacher.cache_manager import CacheManager
from app.db.redis import get_redis
from app.db.postgresql import get_db
from typing import List, Optional, Union

router = APIRouter()


# Dependency to create an instance of BookUseCase
def get_book_usecase():
    repository = BookRepository(db=next(get_db()), cache=CacheManager(get_redis()))
    return BookUseCase(repository)


# API Response Model
class APIResponse(BaseModel):
    data: Optional[Union[BaseModel, dict, List[BaseModel]]] = None
    errors: Optional[dict] = None
    meta: Optional[dict] = None
    status: int


# Response Model for Book Search
class BookSearchResponse(BaseModel):
    items: List[BookSchema]
    total: int
    page: int
    size: int
    sort: List[str]


# Helper function to create a consistent error response
def create_error_response(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=APIResponse(
            data=None,
            errors={"message": message},
            status=status_code
        ).dict()
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, usecase: BookUseCase = Depends(get_book_usecase)):
    try:
        new_book = usecase.create_book(book)
        return APIResponse(data=new_book, status=status.HTTP_201_CREATED)
    except InvalidBookDataError as e:
        return create_error_response("Invalid book data provided.", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return create_error_response("An unexpected error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{book_id}")
def read_book(book_id: int, usecase: BookUseCase = Depends(get_book_usecase)):
    try:
        book = usecase.get_book(book_id)
        return APIResponse(data=book, status=status.HTTP_200_OK)
    except BookNotFoundError as e:
        return create_error_response("Book not found.", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return create_error_response("An unexpected error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
def search_books(
        query: Optional[str] = Query(None),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=20),
        sort: List[str] = Query(["created_at:desc"],
                                description="Sort order, format: field:direction. Example: title:asc"),
        usecase: BookUseCase = Depends(get_book_usecase)
):
    try:
        if page < 1 or size > 20:  # Additional validation logic
            raise ValueError("Invalid search criteria.")

        criteria = BookSearchCriteria(query=query, page=page, size=size, sort=sort)
        books, total = usecase.search_books(criteria)
        response_data = BookSearchResponse(
            items=books,
            total=total,
            page=page,
            size=size,
            sort=sort
        )
        return APIResponse(data=response_data, status=status.HTTP_200_OK)
    except ValueError as e:
        return create_error_response("Invalid search criteria.", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return create_error_response("An unexpected error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{book_id}")
def update_book(book_id: int, book: BookCreate, usecase: BookUseCase = Depends(get_book_usecase)):
    try:
        updated_book = usecase.update_book(book_id, book)
        return APIResponse(data=updated_book, status=status.HTTP_200_OK)
    except BookNotFoundError as e:
        return create_error_response("Book not found.", status.HTTP_404_NOT_FOUND)
    except InvalidBookDataError as e:
        return create_error_response("Invalid book data provided.", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return create_error_response("An unexpected error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{book_id}")
def delete_book(book_id: int, usecase: BookUseCase = Depends(get_book_usecase)):
    try:
        success = usecase.delete_book(book_id)
        return APIResponse(data={}, status=status.HTTP_200_OK) if success else create_error_response("Delete operation failed.", status.HTTP_500_INTERNAL_SERVER_ERROR)
    except BookNotFoundError as e:
        return create_error_response("Book not found.", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return create_error_response("An unexpected error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)

