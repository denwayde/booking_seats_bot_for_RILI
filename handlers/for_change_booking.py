from btns.forCancelBooking import get_bookings
from btns.forChange import get_change_parametr
from db_func import delete_or_insert_data, select_data
from handlers.for_get_name import name_proccessor
from states import SetConfigsToBot
from handlers.for_row import set_row_handler
from handlers.for_set_row import row_handler


async def change_booking(message, state, bot, text, new_state):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text, reply_markup = get_bookings(message.chat.id, 'change_'))
    await state.set_state(new_state)

async def change_booking_parametr(call, state, bot, text, new_state):
    arr = call.data.split('_')
    invintation_code = select_data("select invintation_code from users where telega_id = ? and place = ? and row = ? and num = ? and canceled = 0", (call.message.chat.id, arr[1], arr[2], arr[3],))[0][0]
    await state.update_data(code = invintation_code)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()
    await call.message.answer(text, reply_markup = get_change_parametr(arr))
    await state.set_state(new_state)


async def change_parametr(call, state, bot):
    arr = call.data.split("_")
    if arr[0] == "mesto":
        await name_proccessor(call.message, state, bot, "Выберите пожалуйста область зала", SetConfigsToBot.set_place)
    elif arr[0] == "ryad":
        await set_row_handler(call, state, arr[1], bot, SetConfigsToBot.set_row)
    elif arr[0] == "num":
        await row_handler(call, state, bot, "Выберите пожалуйста место в ряду", SetConfigsToBot.set_new_row)

