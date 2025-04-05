from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from ...services.gemini import gemini_client
from ..states.gemini import Request

router = Router()


@router.message(Command("ai_request"))
async def write_request_handler(message: types.Message, state: FSMContext):
    await message.answer("Please write your request.")
    await state.set_state(Request.write_request)


@router.message(StateFilter(Request.write_request))
async def set_state_write_request(message: types.Message, state: FSMContext):
    await state.update_data(write_request=message.text)
    stored_data = await state.get_data()
    a = await gemini_client.generate_content(stored_data["write_request"])
    await state.clear()
    await message.answer(a.candidates[0].content.parts[0].text)
