import logging

from src.dispatcher import bot, dp, set_commands


async def start_polling():
    """Запуск в режиме поллинга."""
    logging.info("Бот запущен в режиме POLLING")
    await bot.delete_webhook()
    await set_commands()
    await dp.start_polling(bot)
