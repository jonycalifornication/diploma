from aiogram.fsm.state import State, StatesGroup

class Request(StatesGroup):
    write_request = State()