from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Write a request", callback_data="write_request")]]
)


async def search_keyboard(initial: bool = False) -> InlineKeyboardMarkup:
    keyboards = [
        InlineKeyboardButton(text="🔎 Поиск курсов", switch_inline_query_current_chat=""),
        InlineKeyboardButton(text="🔎 Поиск книг", switch_inline_query_current_chat="-b "),
    ]
    if not initial:
        keyboards.append(InlineKeyboardButton(text="Мои курсы", callback_data="my_courses"))

    return InlineKeyboardMarkup(inline_keyboard=[keyboards, [InlineKeyboardButton(text="🔎 Поиск преподавателей", switch_inline_query_current_chat="-i ")]])
