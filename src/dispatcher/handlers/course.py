from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.dispatcher.callback_datas import CourseCallback, CourseQuestionCallback, EnrollmentCallback, ChapterCallback, \
    InstructorCallback
from src.dispatcher.keyboards.keyboard import search_keyboard
from src.dispatcher.messages.course_details import course_details
from src.services.api import api_service
from src.services.gemini import gemini_client

from ..states.gemini import CourseRequest

router = Router()


@router.callback_query(F.data == "my_courses")  # Исправлено с CallbackQuery.data -> F.data
async def my_courses_callback(query: types.CallbackQuery):
    """Обработчик для кнопки 'Мои курсы'."""
    await send_courses(query.message, query.from_user.id)
    await query.answer()


@router.message(Command("my_courses"))
async def my_courses_command(message: types.Message):
    """Обработчик команды /my_courses."""
    await send_courses(message, message.from_user.id)


async def send_courses(destination: types.Message | types.CallbackQuery, telegram_id: int):
    """Отправляет список курсов пользователю в виде интерактивных кнопок."""
    user = await api_service.check_user(telegram_id=telegram_id)
    if not user:
        await destination.answer("Не удалось найти информацию о пользователе. Попробуйте зарегистрироваться.")
        return

    if not user.course:
        await destination.answer(
            text="У вас пока нет курсов. Найдите интересующие курсы с помощью кнопки ниже.",
            reply_markup=await search_keyboard(initial=True),
        )
    else:
        button_rows = [
            [InlineKeyboardButton(text=f"📚 {course.title}", callback_data=CourseCallback(course_id=course.id).pack())]
            for course in user.course
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=button_rows)

        await destination.answer(
            text="Вот список ваших курсов. Нажмите на курс, чтобы узнать больше информации:", reply_markup=keyboard
        )


@router.callback_query(CourseCallback.filter())
async def course_info(callback_query: types.CallbackQuery, callback_data: CourseCallback):
    course_id = callback_data.course_id  # Извлекаем ID курса
    course = await api_service.get_course(course_id=course_id)

    if not course:
        await callback_query.answer("Не удалось получить информации о курсе", show_alert=True)
        return

    unsubscribe_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤔 Задать вопрос", callback_data=CourseQuestionCallback(course_id=course_id).pack()
                ),
                InlineKeyboardButton(
                    text="🤔 Содержание курса",
                    callback_data=ChapterCallback(course_id=course_id).pack(),
                )
            ]
        ]
    )
    if course.cover_url:
        await callback_query.message.reply_photo(
            photo=course.cover_url,  # Ссылка на изображение
            caption=await course_details(course),  # Текст под изображением
            reply_markup=unsubscribe_button,
            parse_mode="HTML",
        )
    else:
        await callback_query.message.answer(
            text=await course_details(course), reply_markup=unsubscribe_button, parse_mode="HTML"
        )


@router.callback_query(CourseQuestionCallback.filter())
async def start_course_question(
    callback_query: types.CallbackQuery,
    callback_data: CourseQuestionCallback,
    state: FSMContext,
):
    """
    Обработчик нажатия на кнопку "Задать вопрос о курсе".
    Запрашивает у пользователя его вопрос.
    """
    await state.update_data(course_id=callback_data.course_id)
    await state.set_state(CourseRequest.question)
    await callback_query.message.answer("Напишите ваш вопрос по курсу.")


@router.message(CourseRequest.question)
async def handle_course_question(message: types.Message, state: FSMContext):
    """
    Получает вопрос пользователя и отправляет его в Gemini API с информацией о курсе.
    """
    user_data = await state.get_data()
    course_id = user_data.get("course_id")

    # Получаем информацию о курсе
    course = await api_service.get_course(course_id=course_id)

    # Отправляем запрос в Gemini API
    response = await gemini_client.generate_content(question=message.text, course=course)
    # Отправляем ответ пользователю
    await message.answer(response.candidates[0].content.parts[0].text)  # Отправляем ответ от Gemini

    # Сбрасываем состояние
    await state.clear()
