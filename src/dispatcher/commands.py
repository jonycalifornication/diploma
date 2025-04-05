from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from src import settings

from .handlers import course, enrollment, gemini, inline_query, message, start, instructor, book, chapter

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Начать работу с ботом"),
            BotCommand(command="/help", description="Получить справку"),
            BotCommand(command="/ai_request  ", description="Написать запрос боту"),
            BotCommand(command="/my_courses", description="Мои курсы"),
        ]
    )


dp.include_router(start.router)
dp.include_router(inline_query.router)
dp.include_router(course.router)
dp.include_router(instructor.router)
dp.include_router(gemini.router)
dp.include_router(enrollment.router)
dp.include_router(message.router)
dp.include_router(book.router)