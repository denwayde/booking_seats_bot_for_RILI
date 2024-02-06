from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def pay_btns() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Повторить платеж", callback_data="payagain"),
        InlineKeyboardButton(text="Написать администратору", callback_data="send_to_admin"),     
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)