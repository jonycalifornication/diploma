from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    telegram_id: int
    full_name: str
    email: EmailStr


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] | None
    total: int
    page: int
    size: int
    pages: int

class BookInfo(BaseModel):
    id: str
    image_url: str
    rating: float | None = None  # Лучше хранить рейтинг как float
    author: str | None = None  # Исправлено
    author_link: str | None = None  # Исправлено
    book_title: str | None = None
    book_description: str | None = None
    book_link: str | None = None

class BookItem(BaseModel):
    id: str
    book_title: str
    author: str | None = None
    image_url: str | None = None
    book_description: str | None = None

class BookListResponse(PaginatedResponse[BookItem]):
    pass

class InstructorData(BaseModel):
    id: str
    name: str


class CourseInfo(BaseModel):
    id: str
    title: str
    description: str | None
    duration: int
    cover_url: str | None
    tags: str | None = None
    instructor: InstructorData


class CourseItem(BaseModel):
    id: str
    title: str
    description: str | None
    duration: int
    cover_url: str | None


class CourseListResponse(PaginatedResponse[CourseItem]):
    pass


class InstructorInfo(BaseModel):
    id: str
    bio: str | None
    email: EmailStr
    name: str
    profile_picture_url: str
    degree: str
    specialization: str


class InstructorItem(BaseModel):
    id: str
    name: str
    profile_picture_url: str
    degree: str
    specialization: str


class InstructorListResponse(PaginatedResponse[InstructorItem]):
    pass

class ChapterInfo(BaseModel):
    id: str
    title: str
    description: str | None

class ChapterItem (BaseModel):
    id: str
    title: str
    order: int

class ChapterListResponse(PaginatedResponse[ChapterItem]):
    pass