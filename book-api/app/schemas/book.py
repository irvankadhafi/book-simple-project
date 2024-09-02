from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class BookBase(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    pages: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp, null if not deleted")

    class Config:
        orm_mode=True


class BookSearchCriteria(BaseModel):
    query: Optional[str] = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=20)
    sort: Optional[List[str]] = Field(default=["created_at:desc"])

    def set_default_value(self):
        if self.page <= 0:
            self.page = 1
        if self.size <= 0:
            self.size = 10
        if self.size > 20:
            self.size = 20
        if not self.sort:
            self.sort = ["created_at:desc"]


def parse_sort_param(sort_param: str) -> tuple:
    parts = sort_param.split(':')
    if len(parts) != 2 or parts[1].lower() not in ['asc', 'desc']:
        raise ValueError(f"Invalid sort parameter: {sort_param}")
    return (parts[0], parts[1].upper())
