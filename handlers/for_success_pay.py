from random import randint
from btns.forSettings import settings_keyboard
from db_func import delete_or_insert_data

async def rub_handler(message, bot, state):
    await bot.delete_message(message.chat.id, message.message_id-1)
    invitation_code = randint(1000, 9999)
    state_data = await state.get_data()
    print(state_data)

    delete_or_insert_data(
        "UPDATE seats SET taken = 1 WHERE place = ? row = ? num = ?",
        (
            state_data['place'],
            state_data['row'],
            state_data['num'],
        )
    )

    delete_or_insert_data(
        "INSERT INTO users(telega_id, user_name, place, row, num, invintation_code, price_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            message.chat.id,
            state_data['name'],
            state_data['place'],
            state_data['row'],
            state_data['num'],
            invitation_code,
            state_data['rub'],
        )
    )
    await message.answer(f"Оплата прошла успешно.\nНа имя: {state_data['name']}\nВаше место: {state_data['place']}, Ряд - {state_data['row']}, Номер - {state_data['num']}\nВаш пригласительный код: <b>{invitation_code}</b>.\nПокажите эти данные при входе в зал.",reply_markup=settings_keyboard() , parse_mode='HTML')
    await state.clear()