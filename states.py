from aiogram.fsm.state import State, StatesGroup

class SetConfigsToBot(StatesGroup):
    set_name = State()
    set_place = State()
    set_row = State()
    set_num = State()
    set_rub = State()
    set_success = State()
    msg_to_admin = State()
    set_cancel_booking = State()
    set_new_row = State()