import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

from src.core.parse_config import parse_config


class Settings(BaseSettings):
    """Настройки приложения."""

    BOT_TOKEN: str
    BOT_MODE: str  # "polling" или "webhook"

    # Настройки вебхуков
    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_URL: str

    # Хост и порты
    HOST: str
    PORT: int

    API_URL: str
    API_TOKEN: str
    GEMINI_API_KEY: str


# Загружаем конфиг
config_file = os.getenv("CONFIG_FILE", "config.dev.yaml")
settings_path = Path(__file__).parent / config_file
yaml_settings = parse_config(str(settings_path))


@lru_cache
async def get_settings() -> Settings:
    """Метод DI для получения настроек."""
    return Settings(**yaml_settings)
