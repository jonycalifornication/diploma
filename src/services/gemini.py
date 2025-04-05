import aiohttp
from pydantic import ValidationError

from src import settings
from src.services.schemas.gemini import GeminiResponse
from src.services.schemas.schemas import CourseItem, CourseInfo


class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.headers = {"Content-Type": "application/json"}

    async def _send_request(self, prompt: str):
        """Общий метод для отправки запросов в Gemini API."""
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        params = {"key": self.api_key}
        print("send r", payload, params)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.base_url, headers=self.headers, params=params, json=payload, ssl=False
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    try:
                        return GeminiResponse(**data)
                    except ValidationError as e:
                        return {"error": f"Validation error: {e}"}
            except aiohttp.ClientError as e:
                return {"error": str(e)}

    async def generate_content(self, question: str, course: CourseInfo = None):
        """
        Генерирует ответ на основе вопроса пользователя.
        Если передан курс, использует его информацию для уточнения ответа.
        """
        if course:
            prompt = f"""
            Вопрос: {question}
            У нас есть информация о курсе "{course.title}":
            Описание: {course.description}
            Преподаватель: {course.instructor.name}
            Продолжительность: {course.duration} часов.

            Используя эти данные, ответь на вопрос.
            """
        else:
            prompt = f"""
            Вопрос: {question}
            В базе данных нет прямого ответа. Используй свои знания, чтобы помочь студенту.
            """

        return await self._send_request(prompt)


gemini_client = GeminiClient()
