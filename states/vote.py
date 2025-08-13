from aiogram.fsm.state import State, StatesGroup


class VoteStates(StatesGroup):
    waiting_for_phone = State()
