from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pydantic import ValidationError

from src.dispatcher.callback_datas import EnrollmentCallback, InstructorCallback, BookCallback, DownloadCallback, \
    CourseQuestionCallback, ChapterCallback
from src.dispatcher.keyboards.keyboard import search_keyboard
from src.dispatcher.messages.course_details import course_details, instructor_details, book_details
from src.dispatcher.states.registration import RegistrationForm
from src.services.api import api_service
from src.services.schemas.schemas import UserCreate

router = Router()


@router.message(RegistrationForm.full_name, F.text)
async def process_fullname(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("📧 Отлично! Теперь укажите свой адрес электронной почты:")
    await state.set_state(RegistrationForm.email)


@router.message(RegistrationForm.email, F.text)
async def process_email(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    full_name = user_data["full_name"]
    email = message.text.strip()

    try:
        user_create = UserCreate(
            telegram_id=message.from_user.id,
            full_name=full_name,
            email=email,  # Здесь проверка EmailStr (pydantic автоматически)
        )
    except ValidationError:
        await message.answer("❌ Введен некорректный email. Пожалуйста, попробуйте снова:")
        return  # остаемся на текущем состоянии (RegistrationForm.email)

    # Если все в порядке — отправляем данные на регистрацию
    result = await api_service.create_user(user_create)

    if not result:
        await message.answer("❌ Ошибка регистрации")
        await state.clear()
    else:
        await message.answer("🎉 Регистрация успешно завершена!", reply_markup=await search_keyboard(initial=True))
        await state.clear()


@router.message()
async def handle_course_by_id(message: types.Message, state: FSMContext):
    """
    Обработчик сообщений, который ищет курс по ID.
    Формат сообщения: course_<course_id>
    """
    telegram_id = message.from_user.id
    user = await api_service.check_user(telegram_id)
    if not user:
        await message.answer("👋 Добро пожаловать! Введите свое полное имя:")
        await state.set_state(RegistrationForm.full_name)
        return

    if message.text.startswith("course_"):
        await message.delete()
        course_id = message.text.split("_", 1)[1]
        course = await api_service.get_course(course_id=course_id)
        if not course:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔎 Поиск курсов", switch_inline_query_current_chat="")]]
            )
            await message.answer("Курс с указанным ID не найден.", reply_markup=keyboard)
            return

        # Формируем ответное сообщение с информацией о курсе
        details = await course_details(course)
        enroll_button = InlineKeyboardMarkup(
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
        # Отображаем либо текст, либо текст с фото
        if course.cover_url:
            await message.answer_photo(
                photo=course.cover_url,  # Отображаем изображение курса
                caption=details,
                reply_markup=enroll_button,
                parse_mode="HTML",
            )
        else:
            await message.answer(text=details, reply_markup=enroll_button, parse_mode="HTML")
        return
    if message.text.startswith("instructor_"):
        await message.delete()
        instructor_id = message.text.split("_", 1)[1]
        instructor = await api_service.get_instructor(instructor_id=instructor_id)
        if not instructor:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔎 Поиск преподавателей", switch_inline_query_current_chat="-i ")]
                ]
            )
            await message.answer("Преподаватель с указанным ID не найден.", reply_markup=keyboard)
        details = await instructor_details(instructor)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Курсы",
                    callback_data=InstructorCallback(
                        instructor_id=instructor.id).pack())
                ]
            ]
        )
        await message.answer_photo(
            photo=instructor.profile_picture_url,  # Отображаем изображение курса
            caption=details,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    if message.text.startswith("book_"):
        await message.delete()
        book_id = message.text.split("_", 1)[1]
        book = await api_service.get_book(book_id=book_id)
        if not book:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔎 Поиск книг", switch_inline_query_current_chat="-b ")]
                ]
            )
            await message.answer("Книга с указанным ID не найден.", reply_markup=keyboard)
        details = await book_details(book)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Перейти к чтению",
                        url=book.book_link  # Это кнопка для перехода по ссылке
                    ),
                    InlineKeyboardButton(
                        text="📥 Скачать книгу",
                        callback_data=DownloadCallback(book_id=book.id).pack()
                    )
                ]
            ]
        )
        await message.answer_photo(
            photo=book.image_url,  # Отображаем изображение курса
            caption=details,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
