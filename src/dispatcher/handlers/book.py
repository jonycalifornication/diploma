from aiogram import Router, types, F

from src.dispatcher.callback_datas import DownloadCallback
from src.services.api import api_service
from aiogram.types import CallbackQuery
router = Router()

@router.callback_query(DownloadCallback.filter())
async def send_book(callback_query: CallbackQuery, callback_data: DownloadCallback):
    book_id = callback_data.book_id
    book = await api_service.get_book(book_id=book_id)

    await callback_query.message.answer_document(
        document=book.book_link,
    )
    await callback_query.answer()
