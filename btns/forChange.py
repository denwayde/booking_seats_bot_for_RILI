from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_change_parametr(arr) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    # buttons = [
    #     [InlineKeyboardButton(text=arr[1], callback_data=f"changeparametr_{arr[1]}")],
    #     [InlineKeyboardButton(text=arr[2], callback_data=f"changeparametr_{arr[2]}"), InlineKeyboardButton(text=arr[3], callback_data=f"changeparametr_{arr[3]}")],
    # ]
    kb.row(InlineKeyboardButton(text = arr[1], callback_data=f"changeparametr_{arr[1]}"))
    kb.row(InlineKeyboardButton(text=f'Ряд {arr[2]}', callback_data=f"changeparametr_{arr[2]}"), InlineKeyboardButton(text=f'Место {arr[3]}', callback_data=f"changeparametr_{arr[3]}"))
    # kb.add(*buttons)
    #kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)