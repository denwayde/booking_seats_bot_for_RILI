import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked
from aiogram.types.message import ContentType
import asyncio
from db_func import delete_or_insert_data, select_data

from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных из файла .env

bot_key = os.getenv('BOT_TOKEN')
payment_key = os.getenv('PAYMENT_TOKEN')
   

class SetConfigsToBot(StatesGroup):
    waiting_for_set_name = State()
    waiting_for_set_place = State()
    waiting_for_set_row = State()
    waiting_for_set_num = State()

# Configure logging
logging.basicConfig(level=logging.INFO)
memstore = MemoryStorage()
# Initialize bot and dispatcher
bot = Bot(token=bot_key)
dp = Dispatcher(bot, storage=memstore)
TESTPAY_TOKEN = payment_key

@dp.message_handler(commands='start', state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте. Напишите ваши ФИО")
    await bot.delete_message(message.chat.id, message["message_id"])
    await state.set_state(SetConfigsToBot.waiting_for_set_name.state)


@dp.message_handler(state=SetConfigsToBot.waiting_for_set_name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(chosen_name=message.text)
    # fio =  message.text.split(" ")
    buttons = [
        types.InlineKeyboardButton(text="Партер", callback_data="parter"),
        types.InlineKeyboardButton(text="Балкон (Центр)", callback_data="balkon_center"),
        types.InlineKeyboardButton(text="Балкон (Правое крыло)", callback_data="balkon_right"),
        types.InlineKeyboardButton(text="Балкон (Левое крыло)", callback_data="balkon_left")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await bot.send_photo(message.chat.id, photo="http://www.gdk-ufa.ru/i/scheme.jpg")
    await message.answer(f"Рады познакомиться {message.text}. Выберите пожалуйста часть зала", reply_markup=keyboard)
    await bot.delete_message(message.chat.id, message["message_id"])
    await state.set_state(SetConfigsToBot.waiting_for_set_place.state)


async def set_place_handler(call, state, message_data):
    # arr = await select_data('SELECT DISTINCT row FROM seats WHERE taken = ? and place = ?', (0, message_data, ))
    # print(arr)
    arr = [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (15,), (16,), (17,), (18,), (19,), (20,), (21,)]
    buttons = []
    for x in arr:
        buttons.append(types.InlineKeyboardButton(text=str(x[0]), callback_data=str(x[0])))
    
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await state.update_data(place=message_data)
    await bot.send_photo(call.message.chat.id, photo="http://www.gdk-ufa.ru/i/scheme.jpg")
    await call.message.answer(f"Выбран: {message_data}. Выберите пожалуйста ряд, в которых остались места", reply_markup=keyboard)
    await bot.delete_message(call.message.chat.id, call.message["message_id"])
    await bot.answer_callback_query(callback_query_id=call.id)
    await state.set_state(SetConfigsToBot.waiting_for_set_row.state)


@dp.callback_query_handler(lambda call: True)
async def set_place_parter1(call: types.CallbackQuery):
    await bot.send_message(call.message.chat.id, "Im works")
    await bot.answer_callback_query(callback_query_id=call.id)
    


# @dp.callback_query_handler(lambda call: call.data == "parter", state=SetConfigsToBot.waiting_for_set_place)
# async def set_place_parter(call: types.CallbackQuery, state: FSMContext):
#     await set_place_handler(call, state, "Партер")

# @dp.callback_query_handler(lambda call: call.data == "balkon_center", state=SetConfigsToBot.waiting_for_set_place)
# async def set_place_center(call: types.CallbackQuery, state: FSMContext):
#     await set_place_handler(call, state, "Балкон (Центр)")

# @dp.callback_query_handler(lambda call: call.data == "balkon_right", state=SetConfigsToBot.waiting_for_set_place)
# async def set_place_right(call: types.CallbackQuery, state: FSMContext):
#     await set_place_handler(call, state, "Балкон (Правое крыло)")

# @dp.callback_query_handler(lambda call: call.data == "balkon_left", state=SetConfigsToBot.waiting_for_set_place)
# async def set_place_left(call: types.CallbackQuery, state: FSMContext):
#     await set_place_handler(call, state, "Балкон (Левое крыло)")





@dp.message_handler(commands='pay')
async def start_pay(message: types.Message):
    await bot.send_invoice(chat_id=message.from_user.id, title="Благотворительный взнос", description="Оплата благотворительного фонда для РИЛИ", payload="charity", provider_token=TESTPAY_TOKEN, currency="RUB", start_parameter="pay_to_RILI_bot", prices=[{'label': 'Руб', 'amount': 150000}])

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "charity":
        #RABOTAEM S POLZOVATELEM
        await bot.send_message(message.from_user.id, "Vse oplacheno")





if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
