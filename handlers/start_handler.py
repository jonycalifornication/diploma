from aiogram import Router
from aiogram.filters import Command
from keyboards.start_keyboard import start_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message):
    await message.answer("Hello, I'm a bot! Use the button below to write a request.", reply_markup = start_keyboard)

