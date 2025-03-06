from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from .states import Request
from ai_core.gemini import gemini_client

router = Router()

@router.callback_query(lambda callback: callback.data == "write_request")
async def write_request_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Please write your request.")
    await state.set_state(Request.write_request)

@router.message(StateFilter(Request.write_request))
async def set_state_write_request(message: types.Message, state: FSMContext):
    await state.update_data(write_request = message.text)
    stored_data = await state.get_data()
    a = await gemini_client.generate_content(stored_data["write_request"])
    await message.answer(a.candidates[0].content.parts[0].text)