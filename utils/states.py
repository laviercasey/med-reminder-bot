from aiogram.fsm.state import State, StatesGroup

class AddPillStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_schedule = State()
    waiting_for_time = State()
    waiting_for_custom_time = State()

class SettingsStates(StatesGroup):
    waiting_for_language = State()

class AdminStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_days = State()
