from btns.forCancelBooking import get_bookings
from db_func import delete_or_insert_data

async def cancel_booking(message, state, text, new_state, bot):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text, reply_markup = get_bookings(message.chat.id))
    await state.set_state(new_state)

#callback_data=f'bookings_{x[3]}_{x[4]}_{x[5]}'
async def cancel_booking1(call, state, bot, text):
    data_arr = call.data.split('_')
    delete_or_insert_data(
        "update seats set taken = 0 where place = ?  and row = ? and num = ?",
        (
            data_arr[1],
            data_arr[2],
            data_arr[3],
        )
    )
    delete_or_insert_data(
        "update users set canceled = 1 where place = ?  and row = ? and num = ?",
        (
            data_arr[1],
            data_arr[2],
            data_arr[3],
        )
    )
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()
    await call.message.answer(text)
    await state.clear()
