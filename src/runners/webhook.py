import asyncio
import logging

from aiogram.types import Update
from aiohttp import web

from src import settings
from src.dispatcher import bot, dp, set_commands


async def handle_update(request: web.Request):
    """Принимаем обновления от Telegram."""
    raw_data = await request.json()
    update = Update.model_validate(raw_data)
    await dp.feed_update(bot, update)
    return web.Response()


async def start_webhook():
    """Запуск в режиме вебхуков."""
    app = web.Application()
    app.router.add_post(settings.WEBHOOK_PATH, handle_update)

    await bot.set_webhook(
        f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}", allowed_updates=["message", "inline_query", "callback_query"]
    )
    logging.info(f"Webhook установлен: {settings.WEBHOOK_URL}")

    await set_commands()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.HOST, settings.PORT)
    await site.start()

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        await bot.delete_webhook()
        logging.info("Webhook удален")
