from btns.forCancelBooking import get_bookings
from btns.forChange import get_change_parametr
from db_func import delete_or_insert_data

async def change_booking(message, state, bot, text, new_state):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text, reply_markup = get_bookings(message.chat.id, 'change_'))
    await state.set_state(new_state)

async def change_booking_parametr(call, state, bot, text, new_state):
    arr = call.data.split('_')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.answer()
    await call.message.answer(text, reply_markup = get_change_parametr(arr))
    await state.set_state(new_state)