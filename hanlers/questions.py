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
        "Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО",
        reply_markup=get_places()
    )
    await state.set_state(SetConfigsToBot.set_name)



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