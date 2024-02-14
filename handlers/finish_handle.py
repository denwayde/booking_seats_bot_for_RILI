from db_func import delete_or_insert_data, select_data
from btns.forSettings import settings_keyboard

async def succeed_changing(call, state, bot, text):
    await bot.delete_message(call.message.chat.id, call.message.message_id-1)
    user_data = await state.get_data()
    await call.answer()
    if not hasattr(user_data, 'place') and not hasattr(user_data, 'row') and hasattr(user_data, 'num'):
        delete_or_insert_data(
            "UPDATE users SET num = ? WHERE invintation_code = ?",
            (user_data['num'], user_data['invintation_code'], )
        )
    elif not hasattr(user_data, 'place') and hasattr(user_data, 'row') and hasattr(user_data, 'num'):
        delete_or_insert_data(
            "UPDATE users SET row = ?, num = ? WHERE invintation_code = ?",
            (user_data['row'], user_data['num'], user_data['invintation_code'], )
        )
    elif hasattr(user_data, 'place') and hasattr(user_data, 'row') and hasattr(user_data, 'num'):
        delete_or_insert_data(
            "UPDATE users SET place = ?, row = ?, num = ? WHERE invintation_code = ?",
            (user_data['place'], user_data['row'], user_data['num'], user_data['invintation_code'], )
        )
    user_db_data = select_data("SELECT*FROM users WHERE invintation_code = ?", (user_data['invintation_code'], ))[0]
    await call.message.answer(
        f"Имя: {user_db_data[2]}\nВаше место: {user_db_data[3]}, Ряд - {user_db_data[4]}, Номер - {user_db_data[5]}\nВаш пригласительный код: <b>{user_db_data[7]}</b>.\nПокажите эти данные при входе в зал.", 
        reply_markup=settings_keyboard(),
        parse_mode='HTML'
        )
    await state.clear()

