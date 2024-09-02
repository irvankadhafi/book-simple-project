from fastapi import APIRouter
from app.delivery.httpsvc.handlers import book_handler

router = APIRouter()

router.include_router(book_handler.router, prefix="/books", tags=["books"])
