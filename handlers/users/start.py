# start.py — to'liq almashtiring

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import aiohttp
import asyncio
import logging

from keyboards.inline.main import get_user_start_inline_keyboard
from keyboards.default.main import get_user_start_keyboard, get_user_get_money_keyboard

user_router = Router()

# ====== BACKEND API ======
API_BASE = "http://167.86.71.176/api/v1"          # sizning backend bazangiz
API_USERS = f"{API_BASE}/users/"                   # user upsert endpoint (DRF plural)
API_REF_GRANT = f"/api/{API_BASE}/referral/grant/"      # ✅ referal grant endpoint (MUHIM)

logger = logging.getLogger("bot.start")

# ----------------- HELPERS -----------------
async def _upsert_user(msg: Message) -> None:
    payload = {
        "user_id": msg.from_user.id,
        "username": msg.from_user.username,
        "full_name": (msg.from_user.full_name or "Unknown").strip(),
        "active": True,
        "language": (getattr(msg.from_user, "language_code", "uz") or "uz").split("-")[0][:2],
    }

    timeout = aiohttp.ClientTimeout(total=10)
    conn = aiohttp.TCPConnector(limit=20, ttl_dns_cache=300)

    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
        try:
            async with session.post(API_USERS, json=payload) as resp:
                text = await resp.text()
                if resp.status in (200, 201, 409):
                    logger.info("User upsert OK: status=%s body=%s", resp.status, text[:300])
                    return
                logger.error("User upsert FAILED: status=%s body=%s", resp.status, text[:1000])
        except Exception as e:
            logger.exception("User upsert exception: %r", e)

def _parse_start_payload(text: str) -> int | None:
    """
    /start <payload> — payload faqat raqam (referrer_id) bo'lsin.
    Masalan, https://t.me/openbudget_humo_bot?start=12345 => /start 12345
    """
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return None
    p = parts[1].strip()
    return int(p) if p.isdigit() else None

async def _grant_referral_if_needed(msg: Message) -> None:
    """
    Agar user referal havola orqali kirgan bo'lsa (payload bor),
    backendga grant so'rovi yuboriladi -> referrening balansiga pul tushadi.
    """
    referrer_id = _parse_start_payload(msg.text)
    if not referrer_id:
        return

    referred_id = msg.from_user.id
    if referrer_id == referred_id:
        return  # o'zini-o'zi taklif qilishni inkor qilamiz

    timeout = aiohttp.ClientTimeout(total=10)
    conn = aiohttp.TCPConnector(limit=20, ttl_dns_cache=300)

    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
        try:
            async with session.post(
                API_REF_GRANT,
                json={"referrer_user_id": referrer_id, "referred_user_id": referred_id},
            ) as resp:
                body = await resp.text()
                if resp.status in (200, 201):
                    logger.info("Referral grant OK: %s %s", resp.status, body[:300])
                else:
                    logger.error("Referral grant FAIL: %s %s", resp.status, body[:1000])
        except Exception as e:
            logger.exception("Referral grant exception: %r", e)

# ----------------- HANDLERS -----------------
@user_router.message(CommandStart())
async def user_start(message: Message):
    # 1) Userni backendga yozamiz (fon rejimida)
    asyncio.create_task(_upsert_user(message))

    # 2) Agar referal payload bo'lsa — grant yuboramiz (fon rejimida)
    asyncio.create_task(_grant_referral_if_needed(message))

    # 3) Xush kelibsiz matn + asosiy menyu
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
        reply_markup=get_user_start_keyboard(),
        parse_mode="HTML",
    )

@user_router.callback_query(F.data == "back_to_home")
async def back_to_home(callback: CallbackQuery):
    await callback.message.edit_text(
        "Quyidagi menyudan kerakli bo‘limni tanlang:",
        reply_markup=get_user_start_inline_keyboard(),
    )
