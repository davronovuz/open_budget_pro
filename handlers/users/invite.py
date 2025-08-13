from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline.user import get_back_to_home_keyboard

invite_router = Router()


@invite_router.callback_query(F.data == "invite")
async def show_invite(callback: CallbackQuery):
    me = await callback.bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{callback.from_user.id}"
    text = (
        "Do'stlaringizni quyidagi havola orqali taklif qiling:\n"
        f"{link}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_home_keyboard(),
    )
