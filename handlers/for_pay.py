async def num_handler(call, state, bot, text ,new_state):
    if '_' in call.data: 
        my_num = call.data.split('_')
        await state.update_data(num = my_num[1])
    # tmp_data = await state.get_data()
    # await state.update_data(tmp_data)
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1))
    await call.message.answer(text)
    await call.answer()
    await state.set_state(new_state)
    #'Напишите пожалуйста сумму пожертвования для РИЛИ'