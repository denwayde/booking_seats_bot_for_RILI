from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder

def get_inline_cancel_murkup() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    #kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        InlineKeyboardButton(text="Отмена", callback_data="cancelButton"),
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def get_cancel_murkup() -> ReplyKeyboardMarkup:
    kb = KeyboardBuilder()
    btns = [
        KeyboardButton(text = "Отмена")
    ]
    kb.add(*btns)
    return kb.as_markup(resize_keyboard = True)

def cancel_btni():
    return InlineKeyboardButton(text="Отмена", callback_data="cancelButton")

def cancel_btnk():
    return KeyboardButton(text="Отмена")