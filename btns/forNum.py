from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_func import select_data

def get_nums(row_num, place) -> InlineKeyboardMarkup:
    arr = select_data('SELECT num FROM seats WHERE taken = ? and row = ? and place = ?', (0, row_num, place, ))
    kb = InlineKeyboardBuilder()
    buttons = []
    for x in arr:
        buttons.append(InlineKeyboardButton(text=str(x[0]), callback_data='num_'+str(x[0])))
    kb.add(*buttons)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
