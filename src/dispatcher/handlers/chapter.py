from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.dispatcher.callback_datas import ChapterCallback, CourseCallback, ChapterInfoCallback
from src.services.api import api_service

router = Router()

@router.callback_query(ChapterInfoCallback.filter())
async def show_chapter_info(callback_query: types.CallbackQuery, callback_data: ChapterInfoCallback):
    """Показывает подробную информацию о главе."""
    chapter_id = callback_data.chapter_id

    chapter = await api_service.get_chapter(chapter_id=chapter_id)

    if not chapter:
        await callback_query.answer("Не удалось получить информацию о главе", show_alert=True)
        return

    course_id = chapter.course_id  # Получаем нужный course_id отсюда

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к списку глав",
                    callback_data=ChapterCallback(course_id=course_id).pack()
                )
            ]
        ]
    )

    await callback_query.message.answer(
        text=f"<b>{chapter.title}</b>\n\n{chapter.description}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(ChapterCallback.filter())
async def show_chapters(callback_query: types.CallbackQuery, callback_data: ChapterCallback):
    """Отображает главы выбранного курса."""
    course_id = callback_data.course_id
    course = await api_service.get_course(course_id=course_id)

    if not course:
        await callback_query.answer("Не удалось получить информацию о курсе", show_alert=True)
        return

    # Получаем список глав для данного курса, используя ваш существующий метод
    chapters_response = await api_service.get_chapter_list(course_id=course_id)

    if not chapters_response or not chapters_response.items:
        await callback_query.message.answer(
            "Для данного курса пока не добавлено содержание."
        )
        return

    chapters = chapters_response.items

    # Сортируем главы по порядку, если это необходимо
    chapters.sort(key=lambda chapter: chapter.order)

    # Создаем кнопки для каждой главы
    button_rows = []
    for chapter in chapters:
        button_rows.append([
            InlineKeyboardButton(
                text=f"{chapter.order}. {chapter.title}",
                callback_data=ChapterInfoCallback(chapter_id=chapter.id).pack()
            )
        ])

    # Добавляем кнопку для возврата к информации о курсе
    button_rows.append([
        InlineKeyboardButton(
            text="⬅️ Назад к курсу",
            callback_data=CourseCallback(course_id=course_id).pack()
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=button_rows)

    await callback_query.message.answer(
        text=f"<b>Содержание курса \"{course.title}\":</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )