from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, PreCheckoutQuery, ContentType
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

@router.message(F.text.isdigit()==False, SetConfigsToBot.set_rub)
async def rub_handler(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Похоже что Вы написали не число. Попробуйте ввести сумму пожертвования снова')
    await state.set_state(SetConfigsToBot.set_rub)

@router.message(F.text.isdigit(), SetConfigsToBot.set_rub)
async def rub_handler(message: Message, state: FSMContext, bot: Bot):
    is_rub = fullmatch(r"\d+", message.text)
    if is_rub:
        await state.update_data(rub = message.text)
        await bot.delete_message(message.chat.id, message.message_id-1)
        my_amount = int(f'{message.text}00')
        await bot.send_invoice(chat_id=message.from_user.id, title="Благотворительный взнос", description="Оплата благотворительного фонда для РИЛИ", payload="charity", provider_token=payment_key, currency="RUB", start_parameter="pay_to_RILI_bot", need_phone_number=True, prices=[{'label': 'Руб', 'amount': my_amount}])

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    print(f'pre_chekaut:{pre_checkout_query}')
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    
    await state.set_state(SetConfigsToBot.set_success)

# "message_id=758 date=datetime.datetime(2024, 2, 1, 10, 11, 17, tzinfo=TzInfo(UTC)) chat=Chat(id=1949640271, type='private', title=None, username='Dinis_Fizik', first_name='Dinis', last_name='R', is_forum=None, photo=None, active_usernames=None, available_reactions=None, accent_color_id=None, background_custom_emoji_id=None, profile_accent_color_id=None, profile_background_custom_emoji_id=None, emoji_status_custom_emoji_id=None, emoji_status_expiration_date=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None, description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None, has_protected_content=None, has_visible_history=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, location=None) message_thread_id=None from_user=User(id=1949640271, is_bot=False, first_name='Dinis', last_name='R', username='Dinis_Fizik', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None) sender_chat=None forward_origin=None is_topic_message=None is_automatic_forward=None reply_to_message=None external_reply=None quote=None via_bot=None edit_date=None has_protected_content=None media_group_id=None author_signature=None text=None entities=None 
# link_preview_options=None animation=None audio=None document=None photo=None sticker=None story=None video=None video_note=None voice=None caption=None caption_entities=None has_media_spoiler=None contact=None dice=None game=None poll=None venue=None location=None new_chat_members=None left_chat_member=None new_chat_title=None new_chat_photo=None delete_chat_photo=None group_chat_created=None supergroup_chat_created=None channel_chat_created=None message_auto_delete_timer_changed=None migrate_to_chat_id=None migrate_from_chat_id=None pinned_message=None invoice=None successful_payment=SuccessfulPayment(currency='RUB', total_amount=90000, invoice_payload='charity', telegram_payment_charge_id='6749302013_1949640271_78493', provider_payment_charge_id='2d4d8203-000f-5000-9000-15fc20582329', shipping_option_id=None, order_info=OrderInfo(name=None, phone_number='79603927490', email=None, shipping_address=None)) users_shared=None chat_shared=None connected_website=None write_access_allowed=None passport_data=None proximity_alert_triggered=None forum_topic_created=None forum_topic_edited=None forum_topic_closed=None forum_topic_reopened=None general_forum_topic_hidden=None general_forum_topic_unhidden=None giveaway_created=None giveaway=None giveaway_winners=None giveaway_completed=None video_chat_scheduled=None video_chat_started=None video_chat_ended=None video_chat_participants_invited=None web_app_data=None reply_markup=None forward_date=None forward_from=None forward_from_chat=None forward_from_message_id=None forward_sender_name=None forward_signature=None user_shared=None"

# "message_id=776 date=datetime.datetime(2024, 2, 1, 10, 17, 16, tzinfo=TzInfo(UTC)) chat=Chat(id=1949640271, type='private', title=None, username='Dinis_Fizik', first_name='Dinis', last_name='R', is_forum=None, photo=None, active_usernames=None, available_reactions=None, accent_color_id=None, background_custom_emoji_id=None, profile_accent_color_id=None, profile_background_custom_emoji_id=None, emoji_status_custom_emoji_id=None, 
# emoji_status_expiration_date=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None, description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None, has_protected_content=None, has_visible_history=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, location=None) message_thread_id=None from_user=User(id=1949640271, is_bot=False, first_name='Dinis', last_name='R', username='Dinis_Fizik', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None) sender_chat=None forward_origin=None is_topic_message=None is_automatic_forward=None reply_to_message=None external_reply=None quote=None via_bot=None edit_date=None has_protected_content=None media_group_id=None author_signature=None text='f3f' entities=None link_preview_options=None animation=None audio=None document=None photo=None sticker=None story=None 
# video=None video_note=None voice=None caption=None caption_entities=None has_media_spoiler=None contact=None dice=None game=None poll=None venue=None location=None new_chat_members=None left_chat_member=None new_chat_title=None 
# new_chat_photo=None delete_chat_photo=None group_chat_created=None supergroup_chat_created=None channel_chat_created=None message_auto_delete_timer_changed=None migrate_to_chat_id=None migrate_from_chat_id=None pinned_message=None invoice=None successful_payment=None users_shared=None chat_shared=None connected_website=None write_access_allowed=None passport_data=None proximity_alert_triggered=None forum_topic_created=None forum_topic_edited=None forum_topic_closed=None forum_topic_reopened=None general_forum_topic_hidden=None general_forum_topic_unhidden=None giveaway_created=None giveaway=None giveaway_winners=None giveaway_completed=None video_chat_scheduled=None video_chat_started=None video_chat_ended=None video_chat_participants_invited=None web_app_data=None reply_markup=None forward_date=None forward_from=None forward_from_chat=None forward_from_message_id=None forward_sender_name=None forward_signature=None user_shared=None"

@router.message(lambda mes: mes.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def rub_handler(message: Message, bot: Bot, state: FSMContext):
    if message.successful_payment!= None: 
        await message.answer(
            'fine'
        )
    else:
        await message.answer('bad')
        state.set_state()
    state_data = await state.get_data()
    #print(state_data)

# @router.message(lambda mes: mes.successful_payment == None)
# async def rub_handler1(message: Message, bot: Bot, state: FSMContext):
#     await message.answer('bad')