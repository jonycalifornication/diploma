from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from src.dispatcher.keyboards.keyboard import search_keyboard
from src.services.api import api_service
from src.dispatcher.states.registration import RegistrationForm

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await api_service.check_user(telegram_id)

    if user:
        await message.answer(
            f"Привет {user.full_name}! Я помогу тебе найти "
            f"курсы или показать твои текущие курсы! Выбери нужную кнопку ниже:",
            reply_markup=await search_keyboard(initial=True),
        )
    else:
        await message.answer("👋 Добро пожаловать! Введите свое полное имя:")
        await state.set_state(RegistrationForm.full_name)
        return