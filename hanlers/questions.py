from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm import StatesGroup, State

from keyboards.for_place import get_places


class SetConfigsToBot(StatesGroup):
    set_name = State()
    set_place = State()

router = Router()  # [1]

@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО"
    )
    await state.set_state(SetConfigsToBot.set_name)

@router.message(SetConfigsToBot.set_name)
async def name_proccessor(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await bot.send_photo()
    await message.answer(
        "Приятно познакомиться. Выберите пожалуйста доступную область зала",
        reply_markup = get_places()
        )
    


# @router.message(F.text.lower() == "да")
# async def answer_yes(message: Message):
#     await message.answer(
#         "Это здорово!",
#         reply_markup=ReplyKeyboardRemove()
#     )

# @router.message(F.text.lower() == "нет")
# async def answer_no(message: Message):
#     await message.answer(
#         "Жаль...",
#         reply_markup=ReplyKeyboardRemove()
#     )