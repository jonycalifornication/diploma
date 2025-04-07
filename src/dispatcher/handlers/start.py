from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src.dispatcher.keyboards.keyboard import search_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    full_name = message.from_user.full_name

    await message.answer(
        f"Привет {full_name}! Я помогу тебе найти "
        f"курсы или показать твои текущие курсы! Выбери нужную кнопку ниже:",
        reply_markup=await search_keyboard(initial=True),
    )
    return