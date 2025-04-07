import logging

import aiohttp

from src import settings
from src.services.schemas.schemas import (
    CourseInfo,
    CourseListResponse,
    InstructorInfo,
    InstructorListResponse,
    UserCreate,
    BookInfo,
    BookListResponse, ChapterListResponse, ChapterInfo, ChapterItem,
)
from src.services.schemas.user import UserResponse


class APIService:
    """Асинхронный класс для взаимодействия с API с инкапсуляцией методов запросов."""

    def __init__(self, api_url: str, api_key: str):
        self.__api_url = api_url
        self.__api_key = api_key
        self.__headers = {"Authorization": f"Bearer {self.__api_key}"}

    async def _request(self, method: str, endpoint: str, params: dict = None, data: dict = None):
        url = f"{self.__api_url}/api/v1/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, json=data, headers=self.__headers) as response:
                if response.status in (200, 201, 202):
                    return await response.json()
                return None

    async def create_user(self, user_data: UserCreate):
        return await self._request("POST", "user", data=user_data.model_dump())

    async def check_user(self, telegram_id: int):
        endpoint = f"user/telegram_id/{telegram_id}"
        res = await self._request("GET", endpoint=endpoint)
        if res:
            return UserResponse(**res)
        return None

    async def get_courses(self, title: str) -> CourseListResponse | None:
        endpoint = f"course/list?page=1&size=40&is_active=true&title={title}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return CourseListResponse(**res)

    async def get_courses_ins(self, instructor_id: str) -> CourseListResponse | None:
        endpoint = f"course/list?page=1&size=40&is_active=true&instructor_id={instructor_id}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return CourseListResponse(**res)

    async def get_course(self, course_id: str):
        endpoint = f"course/{course_id}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return CourseInfo(**res)



    async def enroll_course(self, course_id: str, user_id: str):
        success = await self._request("POST", endpoint="enrollment", data={"course_id": course_id, "user_id": user_id})
        if not success:
            return False
        return True

    async def cancel_enrollment(self, course_id: str, user_id: str):
        success = await self._request("DELETE", endpoint=f"enrollment/{user_id}/{course_id}")
        if not success:
            return False
        return True

    async def get_instructor_list(self, name: str) -> InstructorListResponse | None:
        endpoint = f"instructor/list?page=1&size=50&name={name}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return InstructorListResponse(**res)

    async def get_instructor(self, instructor_id: str):
        endpoint = f"instructor/{instructor_id}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return InstructorInfo(**res)

    async def get_book(self, book_id: str):
        endpoint = f"book/{book_id}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return BookInfo(**res)

    async def get_book_list(self, book_title: str) -> BookListResponse | None:
        endpoint = f"book/list?page=1&size=50&book_title={book_title}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return BookListResponse(**res)

    async def get_chapter_list(self, course_id: str) -> ChapterListResponse | None:
        endpoint = f"chapter/list?page=1&size=10&course_id={course_id}"
        res = await self._request("GET", endpoint=endpoint)
        if not res:
            return None
        return ChapterListResponse(**res)

    async def get_chapter(self, chapter_id: str):
        endpoint = f"chapter/{chapter_id}"
        res = await self._request("GET", endpoint=endpoint)
        logging.info(f"CHAPTER RESPONSE: {res}")
        if res:
            return ChapterItem(**res)  # Предполагаем, что у вас есть модель Chapter
        return None



api_service = APIService(settings.API_URL, settings.API_TOKEN)
