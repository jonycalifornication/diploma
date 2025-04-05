from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.dispatcher.callback_datas import CourseCallback, CourseQuestionCallback, EnrollmentCallback, InstructorCallback
from src.dispatcher.keyboards.keyboard import search_keyboard
from src.dispatcher.messages.course_details import course_details
from src.services.api import api_service
from src.services.gemini import gemini_client

from ..states.gemini import CourseRequest

router = Router()


@router.callback_query(InstructorCallback.filter())
async def course_info(callback_query: types.CallbackQuery, callback_data: InstructorCallback):
    courses_response = await api_service.get_courses_ins(instructor_id=callback_data.instructor_id)
    if not courses_response:
        await callback_query.answer("Не удалось получить информации о курсе", show_alert=True)
        return
    button_rows = [
        [InlineKeyboardButton(text=f"📚 {course.title}", callback_data=CourseCallback(course_id=course.id).pack())]
        for course in courses_response.items
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button_rows)

    await callback_query.message.answer(
        text="Вот список ваших курсов. Нажмите на курс, чтобы узнать больше информации:", reply_markup=keyboard
    )