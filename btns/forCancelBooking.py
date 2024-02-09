from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def get_bookings(message_data, call_start) -> InlineKeyboardMarkup:
    arr = select_data(
        "select * from users where telega_id = ? and canceled = ?",
        (
            message_data,
            0,
        )
    )
    kb = InlineKeyboardBuilder()
    buttons = []
    for x in arr:
        buttons.append(InlineKeyboardButton(text=f'{x[3]} Ряд: {x[4]} Место: {x[5]}', callback_data=f'{call_start}{x[3]}_{x[4]}_{x[5]}'))#bookings_
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)