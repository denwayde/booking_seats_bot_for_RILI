from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from btns.forPlace import get_places
from btns.forNum import get_nums
from functions import set_row_handler
from re import fullmatch
from dotenv import load_dotenv

import os
load_dotenv()  # Загрузка переменных из файла .env
payment_key = os.getenv('PAYMENT_TOKEN')


class SetConfigsToBot(StatesGroup):
    set_name = State()
    set_place = State()
    set_row = State()
    set_num = State()
    set_rub = State()

router = Router()  # [1]

@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО"
    )
    await state.set_state(SetConfigsToBot.set_name)

@router.message(SetConfigsToBot.set_name)
async def name_proccessor(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(name = message.text)
    await bot.delete_message(message.chat.id, message.message_id-1)
    #await message.delete()
    await message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await message.answer(
        "Приятно познакомиться. Выберите пожалуйста область зала",
        reply_markup = get_places()
        )
    await state.set_state(SetConfigsToBot.set_place)



@router.callback_query(F.data.startswith('place_'), SetConfigsToBot.set_place)
async def place_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    message_data = call.data.split('_')
    if message_data[1] == 'parter':
        await set_row_handler(call, state, "Партер", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonCenter':
        await set_row_handler(call, state, "Балкон (Центр)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonRight':
        await set_row_handler(call, state, "Балкон (Правое крыло)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonLeft':
        await set_row_handler(call, state, "Балкон (Левое крыло)", bot, SetConfigsToBot.set_row)


@router.callback_query(F.data.startswith('row_'), SetConfigsToBot.set_row)
async def row_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    row_num = call.data.split('_')
    await state.update_data(row = row_num[1])
    user_data = await state.get_data()
    #print(user_data)
    #await bot.delete_message(call.message.chat.id, call.message.message_id-2)
    await bot.delete_message(call.message.chat.id, call.message.message_id-1)
    await call.message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await call.message.answer(
        f"Вы выбрали:\nОбласть зала - {user_data['place']}\nРяд - №{row_num[1]}.\nВыберите пожалуйста место в ряду",
        reply_markup=get_nums(row_num[1], user_data['place'])
    )
    await call.answer()
    await state.set_state(SetConfigsToBot.set_num)



@router.callback_query(F.data.startswith('num_'), SetConfigsToBot.set_num)
async def num_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    my_num = call.data.split('_')
    await state.update_data(num = my_num[1])
    await bot.delete_message(call.message.chat.id, call.message.message_id-1)
    await call.message.answer('Напишите пожалуйста сумму пожертвования для РИЛИ')
    await call.answer()
    await state.set_state(SetConfigsToBot.set_rub)


@router.message(F.text, SetConfigsToBot.set_rub)
async def rub_handler(message: Message, state: FSMContext, bot: Bot):
    is_rub = fullmatch(r"\d+", message.text)
    if is_rub:
        await state.update_data(rub = message.text)
        await bot.delete_message(message.chat.id, message.message_id-1)
        #await message.amswer(f"Вы ввели: {message.text}.")
        my_amount = int(message.text + str(00))
        await bot.send_invoice(chat_id=message.from_user.id, title="Благотворительный взнос", description="Оплата благотворительного фонда для РИЛИ", payload="charity", provider_token=payment_key, currency="RUB", start_parameter="pay_to_RILI_bot", prices=[{'label': 'Руб', 'amount': my_amount}])