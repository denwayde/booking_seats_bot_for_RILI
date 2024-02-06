async def send_message_to_admin(message, state, bot, text, new_state):
    await state.clear()
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text)
    await state.set_state(new_state)

async def reply_for_msg_to_admin(message, state, bot, text):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text)
    await bot.send_message(1949640271, message.text)
    await state.clear()
