from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def get_rows(message_data) -> InlineKeyboardMarkup:
    arr = select_data('SELECT DISTINCT row FROM seats WHERE taken = ? and place = ?', (0, message_data, ))
    kb = InlineKeyboardBuilder()
    buttons = []
    for x in arr:
        buttons.append(InlineKeyboardButton(text=str(x[0]), callback_data='row_'+str(x[0])))
    kb.add(*buttons)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)