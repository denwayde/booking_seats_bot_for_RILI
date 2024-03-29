from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, PreCheckoutQuery, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import SetConfigsToBot
# from btns.forPlace import get_places
# from btns.forNum import get_nums
from handlers.for_row import set_row_handler
from re import fullmatch
from dotenv import load_dotenv
from btns.forPay import pay_btns
from handlers.for_pay import num_handler
from handlers.for_send_admin import send_message_to_admin, reply_for_msg_to_admin
import os
from handlers.for_start import start_func
from handlers.for_success_pay import rub_handler
from handlers.for_cancel_booking import cancel_booking, cancel_booking1

load_dotenv()  # Загрузка переменных из файла .env
payment_key = os.getenv('PAYMENT_TOKEN')




router = Router()  # [1]

@router.message(Command("start"), StateFilter(None))  # [2]
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await start_func(message, state, 'Здравствуйте, Вас приветсвует бот, который поможет Вам забронировать место в зале. Давайте приступим.\nНапишите пожалуйста боту ФИО', SetConfigsToBot.set_name, bot)

from handlers.for_get_name import name_proccessor
@router.message(SetConfigsToBot.set_name)
async def sss_name(message: Message, state: FSMContext, bot: Bot):
    await name_proccessor(message, state, bot, f"Приятно познакомиться, {message.text}. Выберите пожалуйста область зала", SetConfigsToBot.set_place)



@router.callback_query(F.data.startswith('place_'), SetConfigsToBot.set_place)
async def place_handler(call: CallbackQuery, state: FSMContext, bot: Bot):#vot tut ty konechno tupanul b..
    message_data = call.data.split('_')
    if message_data[1] == 'parter':
        await set_row_handler(call, state, "Партер", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonCenter':
        await set_row_handler(call, state, "Балкон (Центр)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonRight':
        await set_row_handler(call, state, "Балкон (Правое крыло)", bot, SetConfigsToBot.set_row)
    elif message_data[1] == 'balkonLeft':
        await set_row_handler(call, state, "Балкон (Левое крыло)", bot, SetConfigsToBot.set_row)


from handlers.for_set_row import row_handler
@router.callback_query(F.data.startswith('row_'), SetConfigsToBot.set_row)
async def sss_row_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    await row_handler(call, state, bot, f"Вы выбрали:\nОбласть зала - {user_data['place']}\nРяд - №{call.data.split('_')[1]}.\nВыберите пожалуйста место в ряду", SetConfigsToBot.set_num)


from handlers.finish_handle import succeed_changing
@router.callback_query(F.data.startswith('num_'), SetConfigsToBot.set_num)
async def nnn(call:CallbackQuery, state: FSMContext, bot: Bot):
    is_code = await state.get_data()
    if hasattr(is_code, 'code'):
        await succeed_changing(call, state, bot)
    else:
        await num_handler(call, state, bot, "Напишите пожалуйста сумму пожертвования", SetConfigsToBot.set_rub)


@router.message(F.text.isdigit()==False, SetConfigsToBot.set_rub)
async def rub_handler1(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Похоже что Вы написали не число. Попробуйте ввести сумму пожертвования снова')
    await state.set_state(SetConfigsToBot.set_rub)


@router.message(F.text.isdigit(), SetConfigsToBot.set_rub)
async def rub_handler2(message: Message, state: FSMContext, bot: Bot):
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
    

@router.callback_query(F.data == "payagain")
async def nnnn(call: CallbackQuery, state: FSMContext, bot: Bot):
    await num_handler(call, state, bot, 'Проверьте баланс Вашей карты. Или измените сумму платежа и попробуйте ввести эту сумму.', SetConfigsToBot.set_rub)


@router.message(lambda mes: mes.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def rub_ssss(message: Message, bot: Bot, state: FSMContext):
    await rub_handler(message, bot, state)


@router.message(F.text == "Написать администратору бота", StateFilter(None))
async def sss(message:Message, state: FSMContext, bot: Bot):
    await send_message_to_admin(message, state, bot, 'Напишите сообщение администратору. Если захотите получить обратную связь напишите ссылку на ваш аккаунт в телеграмме.', SetConfigsToBot.msg_to_admin)

@router.message(SetConfigsToBot.msg_to_admin)
async def sss1(message:Message, state:FSMContext, bot:Bot):
    await reply_for_msg_to_admin(message, state, bot, "Ваше сообщения отправлено администратору. При необходимости он с Вами свяжется")


@router.message(F.text == "Забронировать еще место", StateFilter(None))
async def zabronirovat_eshe(message:Message, state: FSMContext, bot: Bot):
    await start_func(message, state, 'Напишите пожалуйста ФИО, для кого нужно забронировать место', SetConfigsToBot.set_name, bot)


@router.message(F.text == "Отменить бронь", StateFilter(None))
async def cancel_process(message:Message, state: FSMContext, bot: Bot):
    await cancel_booking(message, state, 'Выберите пожалуйста бронь для отмены', SetConfigsToBot.set_cancel_booking, bot)

@router.callback_query(F.data.startswith('bookings_'), SetConfigsToBot.set_cancel_booking)
async def cancel_process1(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cancel_booking1(call, state, bot, 'Выбранная Вами бронь отменена. Модераторы бота, переведут Вам Ваши средства в банк привязанный к Вашему номеру телефона. Или свяжутся с Вами по указанному номеру.')


from handlers.for_change_booking import change_booking, change_booking_parametr, change_parametr
@router.message(F.text == "Изменить место", StateFilter(None))
async def change_process(message:Message, state: FSMContext, bot: Bot):
    await change_booking(message, state, bot, 'Выберите бронь, которую нужно изменить', SetConfigsToBot.set_change_booking)


@router.callback_query(F.data.startswith('change_'), SetConfigsToBot.set_change_booking)
async def change_process1(call: CallbackQuery, state: FSMContext, bot: Bot):
    await change_booking_parametr(call, state, bot, 'Выберите параметр брони, который нужно изменить', SetConfigsToBot.set_parametr_change_booking)


@router.callback_query(F.data.startswith('changeParametr_'), SetConfigsToBot.set_change_booking)
async def change_process2(call: CallbackQuery, state: FSMContext, bot: Bot):
    await change_parametr(call, state, bot)


# @router.callback_query(F.data.startswith('change_'), SetConfigsToBot.set_new_row)
# async def change_process3(call: CallbackQuery, state: FSMContext, bot: Bot):
    