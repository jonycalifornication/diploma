import logging
from functools import wraps

from src import settings
from src.runners.polling import start_polling
from src.runners.webhook import start_webhook


def bot_mode(func):
    """Декоратор, который выбирает режим запуска бота."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if settings.BOT_MODE == "polling":
            logging.info("Запускаем бота в режиме POLLING")
            await start_polling()
        elif settings.BOT_MODE == "webhook":
            logging.info("Запускаем бота в режиме WEBHOOK")
            await start_webhook()
        else:
            logging.error("Некорректный режим! Используйте 'polling' или 'webhook'.")
            return

    return wrapper
