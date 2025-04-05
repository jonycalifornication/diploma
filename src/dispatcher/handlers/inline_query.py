import logging
from uuid import uuid4

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from pydantic import ValidationError

from src.services.api import api_service

router = Router()

async def search_books(query_text: str) -> list[InlineQueryResultArticle]:
    """Поиск преподавателей."""
    results = []
    book_title = query_text[3:].strip()

    if not book_title:
        return results

    books_response = await api_service.get_book_list(book_title=book_title)

    if not books_response or not books_response.items:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Книги не найдены",
                description="Попробуйте изменить запрос",
                input_message_content=InputTextMessageContent(
                    message_text="Книги не найдены. Попробуйте изменить запрос или уточнить название."
                ),
            )
        )
    else:
        for book in books_response.items:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=book.book_title,
                    description=f"{book.author} | {book.book_description}",
                    thumbnail_url=book.image_url,
                    input_message_content=InputTextMessageContent(message_text=f"book_{book.id}"),
                )
            )

    return results

async def search_instructors(query_text: str) -> list[InlineQueryResultArticle]:
    """Поиск преподавателей."""
    results = []
    instructor_name = query_text[3:].strip()

    if not instructor_name:
        return results

    instructors_response = await api_service.get_instructor_list(name=instructor_name)

    if not instructors_response or not instructors_response.items:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Преподаватели не найдены",
                description="Попробуйте изменить запрос",
                input_message_content=InputTextMessageContent(
                    message_text="Преподаватели не найдены. Попробуйте изменить запрос."
                ),
            )
        )
    else:
        for instructor in instructors_response.items:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=instructor.name,
                    description=f"Специализация: {instructor.specialization} | {instructor.degree}",
                    thumbnail_url=instructor.profile_picture_url,
                    input_message_content=InputTextMessageContent(message_text=f"instructor_{instructor.id}"),
                )
            )

    return results


async def search_courses(query_text: str) -> list[InlineQueryResultArticle]:
    """Поиск курсов."""
    results = []
    courses_response = await api_service.get_courses(title=query_text)

    if not courses_response.items:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Курсы не найдены",
                description="Попробуйте изменить запрос",
                input_message_content=InputTextMessageContent(
                    message_text="Курсы не найдены. Попробуйте изменить запрос или уточнить название."
                ),
            )
        )
    else:
        for course in courses_response.items:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=course.title,
                    description=f"{course.duration} ч | {course.description}",
                    thumbnail_url=course.cover_url,
                    input_message_content=InputTextMessageContent(message_text=f"course_{course.id}"),
                )
            )

    return results


@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    """Инлайн-поиск курсов или преподавателей."""
    query_text = inline_query.query.strip()

    if not query_text:
        await inline_query.answer([])
        return

    try:
        logging.info(f"Получен инлайн запрос: {query_text}")

        if query_text.startswith("-i"):
            results = await search_instructors(query_text)
        elif query_text.startswith("-b"):
            results = await search_books(query_text)
        else:
            results = await search_courses(query_text)

        await inline_query.answer(results, cache_time=1, is_personal=True)

    except ValidationError as e:
        logging.error(f"Ошибка валидации: {e}")
        await inline_query.answer([])
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
        await inline_query.answer([])

