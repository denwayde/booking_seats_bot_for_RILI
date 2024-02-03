from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def settings_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    # kb.button(text="Да")
    # kb.button(text="Нет")
    buttons = [
        KeyboardButton(text="Забронировать еще место"),
        KeyboardButton(text="Изменить место"),
        KeyboardButton(text="Отменить бронь"),
        KeyboardButton(text="Написать администратору бота")
    ]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)