import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from infrastructure.database.utils import session_pool
from infrastructure.database.models import Project, Vote
from keyboards.inline.main import get_user_start_inline_keyboard
from keyboards.inline.user import get_projects_keyboard, get_back_to_home_keyboard
from states import VoteStates

vote_router = Router()


@vote_router.callback_query(F.data == "vote")
async def list_projects(callback: CallbackQuery):
    async with session_pool() as session:
        result = await session.execute(select(Project).where(Project.is_active == True))
        projects = result.scalars().all()
    if not projects:
        await callback.message.edit_text(
            "Hozir aktiv loyihalar mavjud emas.",
            reply_markup=get_back_to_home_keyboard(),
        )
        return
    await callback.message.edit_text(
        "Ovoz bermoqchi bo'lgan loyihani tanlang:",
        reply_markup=get_projects_keyboard(projects),
    )


@vote_router.callback_query(F.data.startswith("project:"))
async def ask_phone(callback: CallbackQuery, state: FSMContext):
    project_id = int(callback.data.split(":", 1)[1])
    await state.update_data(project_id=project_id)
    await state.set_state(VoteStates.waiting_for_phone)
    await callback.message.edit_text(
        "Telefon raqamingizni kiriting (998901234567):",
        reply_markup=get_back_to_home_keyboard(),
    )


@vote_router.message(VoteStates.waiting_for_phone)
async def save_vote(message: Message, state: FSMContext):
    digits = re.sub(r"\D", "", message.text or "")
    if len(digits) != 12:
        await message.answer("Raqam noto'g'ri formatda. Qayta kiriting:")
        return
    data = await state.get_data()
    project_id = data["project_id"]
    async with session_pool() as session:
        vote = Vote(
            user_id=message.from_user.id,
            project_id=project_id,
            phone_snapshot=digits,
            status="PENDING",
        )
        session.add(vote)
        await session.commit()
    await state.clear()
    await message.answer(
        "So'rov qabul qilindi. OTP ni kiritish orqali ovoz berish jarayoni yakunlanadi.",
        reply_markup=get_user_start_inline_keyboard(),
    )
