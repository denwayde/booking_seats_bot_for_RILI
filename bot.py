import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked

class SetConfigsToBot(StatesGroup):
    waiting_for_set_name = State()
    waiting_for_set_row = State()
    waiting_for_set_place = State()

# Configure logging
logging.basicConfig(level=logging.INFO)
memstore = MemoryStorage()
# Initialize bot and dispatcher
bot = Bot(token="")
dp = Dispatcher(bot, storage=memstore)

@dp.message_handler(commands='start', state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте. Напишите ваши ФИО")
    await bot.delete_message(message.chat.id, message["message_id"])
    await state.set_state(SetConfigsToBot.waiting_for_set_name.state)


@dp.message_handler(state=SetConfigsToBot.waiting_for_set_name)
async def choosen_country_handler(message: types.Message, state: FSMContext):

    await state.update_data(chosen_name=message.text)
    fio =  message.text.split(" ")
    await message.answer(f"Рады познакомиться {fio[1]} {fio[2]}. Выберите пожалуйста ряд")
    await bot.send_photo(message.chat.id, photo="http://www.gdk-ufa.ru/i/scheme.jpg")
    await bot.delete_message(message.chat.id, message["message_id"])
    await state.set_state(SetConfigsToBot.waiting_for_set_row.state)



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
