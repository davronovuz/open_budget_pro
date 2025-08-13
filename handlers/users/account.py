from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select, func

from infrastructure.database.utils import session_pool
from infrastructure.database.models import User, Transaction
from keyboards.inline.user import get_back_to_home_keyboard

account_router = Router()


@account_router.callback_query(F.data == "account")
async def show_account(callback: CallbackQuery):
    async with session_pool() as session:
        user = await session.get(User, callback.from_user.id)
        balance = 0  # Balance field not yet implemented
        result = await session.execute(
            select(func.count()).select_from(
                select(Transaction.id)
                .where(Transaction.user_id == callback.from_user.id)
                .subquery()
            )
        )
        tx_count = result.scalar_one()
    text = f"Balansingiz: {balance} so'm\nTranzaksiyalar soni: {tx_count}"
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_home_keyboard(),
    )
