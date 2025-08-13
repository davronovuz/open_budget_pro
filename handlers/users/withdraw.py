from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from infrastructure.database.utils import session_pool
from infrastructure.database.models import Withdrawal
from keyboards.inline.user import get_back_to_home_keyboard
from states import WithdrawStates

withdraw_router = Router()


@withdraw_router.callback_query(F.data == "withdraw")
async def ask_amount(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WithdrawStates.waiting_for_amount)
    await callback.message.edit_text(
        "Yechmoqchi bo'lgan summani kiriting (so'm):",
        reply_markup=get_back_to_home_keyboard(),
    )


@withdraw_router.message(WithdrawStates.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqam kiriting:")
        return
    await state.update_data(amount=int(message.text))
    await state.set_state(WithdrawStates.waiting_for_destination)
    await message.answer("Karta yoki hamyon raqamini kiriting:")


@withdraw_router.message(WithdrawStates.waiting_for_destination)
async def create_withdrawal(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    destination = message.text.strip()
    async with session_pool() as session:
        withdrawal = Withdrawal(
            user_id=message.from_user.id,
            amount_sum=amount,
            method="manual",
            destination_masked=destination,
            status="PENDING",
        )
        session.add(withdrawal)
        await session.commit()
    await state.clear()
    await message.answer(
        "Pul yechish so'rovi yuborildi.",
        reply_markup=get_back_to_home_keyboard(),
    )


@withdraw_router.callback_query(F.data == "my_withdraw_requests")
async def list_requests(callback: CallbackQuery):
    async with session_pool() as session:
        result = await session.execute(
            select(Withdrawal)
            .where(Withdrawal.user_id == callback.from_user.id)
            .order_by(Withdrawal.created_at.desc())
        )
        withdrawals = result.scalars().all()
    if not withdrawals:
        text = "Sizda hali so'rovlar yo'q."
    else:
        lines = [f"{w.amount_sum} so'm - {w.status}" for w in withdrawals]
        text = "\n".join(lines)
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_home_keyboard(),
    )
