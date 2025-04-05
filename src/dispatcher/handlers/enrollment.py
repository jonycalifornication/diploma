from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.dispatcher.callback_datas import EnrollmentCallback
from src.dispatcher.messages.course_details import course_details
from src.services.api import api_service

router = Router()


@router.callback_query(EnrollmentCallback.filter())
async def handle_course_enrollment(callback_query: CallbackQuery, callback_data: EnrollmentCallback):
    """
    Обработчик записи или отписки от курса (в зависимости от course_enroll).
    :param callback_query: CallbackQuery объект от Telegram.
    :param callback_data: Распарсенный callback_data, содержит данные из фабрики (course_id и course_enroll).
    """
    course_id = callback_data.course_id  # Извлекаем ID курса
    course_enroll = callback_data.course_enroll  # Булевое значение: записать (True) или отписать (False)
    telegram_id = callback_query.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    user = await api_service.check_user(telegram_id=telegram_id)

    if not user:
        # Если пользователя не существует
        await callback_query.answer(text="Не удалось найти вашу информацию.")
        return

    if course_enroll:  # Если True - записываем на курс
        success = await api_service.enroll_course(course_id=course_id, user_id=user.id)
        if success:
            await callback_query.answer(text="Вы успешно записаны на курс 🎉")
        else:
            await callback_query.answer(text="Не удалось записаться на курс. Попробуйте позже.")
    else:  # Если False - выполняем отписку от курса
        success = await api_service.cancel_enrollment(course_id=course_id, user_id=user.id)
        if success:
            await callback_query.answer(text="Вы успешно отписались от курса!")
        else:
            await callback_query.answer(text="Не удалось отписаться от курса.", show_alert=True)

    # Получаем актуальную информацию о курсе
    course = await api_service.get_course(course_id=course_id)
    if not course:
        # Если данные курса не удалось получить
        await callback_query.message.edit_text("Обновление данных о курсе не удалось.", parse_mode="HTML")
        return

    # Генерируем обновлённый callback_data с противоположным состоянием для кнопки
    updated_callback_data = EnrollmentCallback(course_enroll=not course_enroll, course_id=course.id).pack()

    # Обновляем кнопки (либо записаться, либо отписаться)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Записаться" if not course_enroll else "Отписаться",
                    callback_data=updated_callback_data,
                )
            ]
        ]
    )

    if course.cover_url:
        # Если у курса есть изображение
        await callback_query.message.edit_caption(
            caption=await course_details(course), reply_markup=keyboard, parse_mode="HTML"
        )
    else:
        # Если изображения нет
        await callback_query.message.edit_text(
            text=await course_details(course), reply_markup=keyboard, parse_mode="HTML"
        )
