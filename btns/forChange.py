from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_change_parametr(arr) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text = arr[1], callback_data=f"changeParametr_mesto_{arr[1]}"))
    kb.row(InlineKeyboardButton(text=f'Ряд {arr[2]}', callback_data=f"changeParametr_ryad_{arr[2]}"), InlineKeyboardButton(text=f'Место {arr[3]}', callback_data=f"changeParametr_num_{arr[3]}"))
    return kb.as_markup(resize_keyboard=True)