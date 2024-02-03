from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, PreCheckoutQuery, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from btns.forPlace import get_places
from btns.forNum import get_nums
from handlers.for_row import set_row_handler
from re import fullmatch
from dotenv import load_dotenv
from btns.forPay import pay_btns
from handlers.for_pay import num_handler
from btns.forSettings import settings_keyboard
from random import randint

import os
load_dotenv()  # Загрузка переменных из файла .env
payment_key = os.getenv('PAYMENT_TOKEN')


class SetConfigsToBot(StatesGroup):
    set_name = State()
    set_place = State()
    set_row = State()
    set_num = State()
    set_rub = State()
    set_success = State()

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
    await bot.delete_messages(message.chat.id, (message.message_id, message.message_id-1))
    #await message.delete()
    await message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await message.answer(
        f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала",
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
    await bot.delete_messages(call.message.chat.id, (call.message.message_id, call.message.message_id-1, ))
    await call.message.answer_photo('http://www.gdk-ufa.ru/i/scheme.jpg')
    await call.message.answer(
        f"Вы выбрали:\nОбласть зала - {user_data['place']}\nРяд - №{row_num[1]}.\nВыберите пожалуйста место в ряду",
        reply_markup=get_nums(row_num[1], user_data['place'])
    )
    await call.answer()
    await state.set_state(SetConfigsToBot.set_num)



@router.callback_query(F.data.startswith('num_'), SetConfigsToBot.set_num)
async def nnn(call:CallbackQuery, state: FSMContext, bot: Bot):
    await num_handler(call, state, bot, "Напишите пожалуйста сумму пожертвования", SetConfigsToBot.set_rub)


@router.message(F.text.isdigit()==False, SetConfigsToBot.set_rub)
async def rub_handler(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Похоже что Вы написали не число. Попробуйте ввести сумму пожертвования снова')
    await state.set_state(SetConfigsToBot.set_rub)


@router.message(F.text.isdigit(), SetConfigsToBot.set_rub)
async def rub_handler(message: Message, state: FSMContext, bot: Bot):
    is_rub = fullmatch(r"\d+", message.text)
    if is_rub:
        await state.update_data(rub = message.text)
        await bot.delete_message(message.chat.id, message.message_id)
        my_amount = int(f'{message.text}00')
        await bot.send_invoice(chat_id=message.from_user.id, title="Благотворительный взнос", description="Оплата благотворительного фонда для РИЛИ", payload="charity", provider_token=payment_key, currency="RUB", start_parameter="pay_to_RILI_bot", need_phone_number=True, prices=[{'label': 'Руб', 'amount': my_amount}])

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    #print(f'pre_chekaut:{pre_checkout_query}')
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await bot.send_message(pre_checkout_query.from_user.id, 'Если вдруг оплата не прошла по техническим причинам, Вы можете повторить платеж.', reply_markup=pay_btns())
    

@router.callback_query(F.data == "pay_again")
async def nnnn(call: CallbackQuery, state: FSMContext, bot: Bot):
    await num_handler(call, state, bot, 'Введите пожалуйста сумму платежа', SetConfigsToBot.set_rub)



@router.message(lambda mes: mes.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def rub_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id-1)
    invitation_code = randint(1000, 9999)
    state_data = await state.get_data()
    print(state_data)
    await message.answer(f"Оплата прошла успешно.\nНа имя: {state_data['name']}\nВаше место: {state_data['place']}, Ряд - {state_data['row']}, Номер - {state_data['num']}\nВаш пригласительный код: <b>{invitation_code}</b>.\nПокажите эти данные при входе в зал.",reply_markup=settings_keyboard() , parse_mode='HTML')
    
    await state.clear()
    #print(state_data)



# @router.message(lambda mes: mes.successful_payment == None)
# async def rub_handler1(message: Message, bot: Bot, state: FSMContext):
#     await message.answer('bad')