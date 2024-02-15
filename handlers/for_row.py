from btns.forRows import get_rows

async def set_row_handler(call, state, message_data, bot, state_param):
    await state.update_data(place = message_data)
    await call.message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await call.message.answer(
         f"Вы выбрали {message_data}. Выберите пожалуйста ряд.",
        reply_markup = get_rows(message_data)
    )
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.answer()
    await state.set_state(state_param)