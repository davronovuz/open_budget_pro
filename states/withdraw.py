from aiogram.fsm.state import State, StatesGroup


class WithdrawStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_destination = State()
