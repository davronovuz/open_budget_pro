from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import aiohttp

from keyboards.inline.main import get_user_start_inline_keyboard

user_router = Router()

API_BASE = "http://144.91.113.85:8088/api/v1"


async def _upsert_user(session: aiohttp.ClientSession, msg: Message) -> None:
    """POST /users/ — idempotent: 200/201/409 = success.
    409 (Conflict) holatini ham mavjud user sifatida qabul qilamiz.
    """
    payload = {
        "user_id": msg.from_user.id,
        "username": msg.from_user.username,
        "full_name": (msg.from_user.full_name or "Unknown").strip(),
        "active": True,
        "language": (getattr(msg.from_user, "language_code", "uz") or "uz").split("-")[0][:2],
    }
    async with session.post(f"{API_BASE}/users/", json=payload, timeout=8) as resp:
        # 200 OK (updated) / 201 Created (new) / 409 Conflict (already exists) — barchasini success deb hisoblaymiz
        if resp.status in {200, 201, 409}:
            return
        # boshqa holatlarda faqat log uchun matn o‘qib olamiz (bot foydalanuvchisini bezovta qilmaymiz)
        _ = await resp.text()
        # agar xohlasangiz: logging.warning(f"User upsert failed: {resp.status} {_}")


@user_router.message(CommandStart())
async def user_start(message: Message):
    # 1) API orqali user'ni ro‘yxatdan o‘tkazish (idempotent)
    try:
        async with aiohttp.ClientSession() as session:
            await _upsert_user(session, message)
    except Exception:
        # server vaqtinchalik yo‘qligida ham /start oqimi to‘xtamasin
        pass

    # 2) xush kelibsiz va menyu
    full_name = (message.from_user.full_name or "Unknown").strip()
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
