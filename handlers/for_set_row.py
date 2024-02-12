from btns.forNum import get_nums
from db_func import delete_or_insert_data
async def row_handler(call, state, bot, text, new_state):
    row_num = call.data.split('_')
    await state.update_data(row = row_num[1])
    user_data = await state.get_data()
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await call.message.answer(text, reply_markup=get_nums(row_num[1], user_data['place'])
    )
    await call.answer()
    await state.set_state(new_state)

    # text =  f"Вы выбрали:\nОбласть зала - {user_data['place']}\nРяд - №{row_num[1]}.\nВыберите пожалуйста место в ряду"
    # new_state = SetConfigsToBot.set_num