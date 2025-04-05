from pydantic import BaseModel, EmailStr

from src.services.schemas.schemas import InstructorData


class Course(BaseModel):
    id: str
    title: str
    description: str
    duration: int
    tags: str
    instructor: InstructorData
    cover_url: str | None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    telegram_id: int
    course: list[Course] | None
