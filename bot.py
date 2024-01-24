import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked
from aiogram.types.message import ContentType

from db_func import delete_or_insert_data, select_data

from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных из файла .env

bot_key = os.getenv('BOT_TOKEN')
payment_key = os.getenv('PAYMENT_TOKEN')
   

class SetConfigsToBot(StatesGroup):
    waiting_for_set_name = State()
    waiting_for_set_row = State()
    waiting_for_set_place = State()

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
    fio =  message.text.split(" ")
    arr = select_data('SELECT DISTINCT row FROM seats WHERE taken = ?', (0,))
    # buttons = [
    #     types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
    #     types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
    #     types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    # ]
    buttons = []
    for x in arr:
        buttons.append(types.InlineKeyboardButton(text=x[0], callback_data=x[0]))
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await message.answer(f"Рады познакомиться {fio[1]} {fio[2]}. Выберите пожалуйста ряд", reply_markup=keyboard)
    await bot.send_photo(message.chat.id, photo="http://www.gdk-ufa.ru/i/scheme.jpg")
    await bot.delete_message(message.chat.id, message["message_id"])
    await state.set_state(SetConfigsToBot.waiting_for_set_row.state)



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
