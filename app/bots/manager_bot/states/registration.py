from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_name = State()
    waiting_email = State()
    waiting_phone = State()
    waiting_role = State()
    confirm = State()
