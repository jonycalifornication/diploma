import os
import aiohttp
from dotenv import load_dotenv
from pydantic import ValidationError

from ai_core.schemas import GeminiResponse


class GeminiClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }

    async def generate_content(self, prompt: str):
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        params = {"key": self.api_key}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                        self.base_url,
                        headers=self.headers,
                        params=params,
                        json=payload,
                        ssl=False
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    try:
                        validated_data = GeminiResponse(**data)
                        return validated_data
                    except ValidationError as e:
                        return {"error": f"Validation error: {e}"}

            except aiohttp.ClientError as e:
                return {"error": str(e)}

gemini_client = GeminiClient()


