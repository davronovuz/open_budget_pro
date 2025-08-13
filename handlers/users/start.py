from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from infrastructure.database.utils import session_pool
from keyboards.inline.main import get_user_start_inline_keyboard
from infrastructure.database.models import User

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    async with session_pool() as session:
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name or "Unknown"

        existing_user = await session.get(User, user_id)
        if not existing_user:
            new_user = User(
                user_id=user_id,
                username=username,
                full_name=full_name,
                active=True,
                language="en",
            )
            session.add(new_user)
            await session.commit()

    welcome_message = f"""
<b>👋 Salom {full_name}!</b>
   Ijtimoiy loyihalarga <b>ovoz berib</b> pul ishlang,
👥 Do‘stlaringizni botga taklif qilib <b>referal bonuslar</b> oling,
💳 To‘plangan balansingizni <b>real pul</b> sifatida yechib oling.

⚠️ Har bir telefon raqam faqat <b>bitta marta</b> ovoz bera oladi.
👇 Quyidagi tugmalardan birini tanlab, davom eting:
    """

    await message.reply(
        welcome_message,
        reply_markup=get_user_start_inline_keyboard(),
        parse_mode="HTML",
    )


@user_router.callback_query(F.data == "back_to_home")
async def back_to_home(callback: CallbackQuery):
    await callback.message.edit_text(
        "Quyidagi menyudan kerakli bo‘limni tanlang:",
        reply_markup=get_user_start_inline_keyboard(),
    )
