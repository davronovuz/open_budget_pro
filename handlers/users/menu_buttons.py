# handlers/users/menu_buttons.py
# Aiogram v3 — ONLY button handlers (no /start). Clean, fast, and extensible.
# - "💰 Hisobim": pulls balance from backend API and shows it
# - Other buttons: placeholder message for now
# - Pretty formatting, safe HTTP, and tidy structure

import os
import asyncio
from typing import Any, Dict

import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction

from handlers.users.payment_user import API_HAS_OPEN, main_menu_keyboard
from keyboards.default.main import get_user_start_keyboard, get_user_get_money_keyboard



HTTP_TIMEOUT = aiohttp.ClientTimeout(total=10)
API_BASE = "http://167.86.71.176/api/v1/api"
BALANCE_ENDPOINT = f"{API_BASE}/balance"


async def has_open_request(user_id: int) -> bool:
    """Backenddan foydalanuvchida tugallanmagan so‘rov bor-yo‘qligini tekshirish"""
    url = f"{API_HAS_OPEN}?user_id={user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("has_open", False)
            return False


menu_router = Router(name="menu_buttons")



def format_sum(value: Any) -> str:
    """Format integer/decimal to spaced thousands: 1234567 -> '1 234 567'"""
    try:
        n = int(float(value))
    except Exception:
        return str(value)
    return f"{n:,}".replace(",", " ")


async def fetch_json(url: str) -> Dict[str, Any] | None:
    async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def send_typing(message: Message, seconds: float = 0.5) -> None:
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(seconds)


PLACEHOLDER = (
    "⚙️ Bu bo'lim tez orada ishga tushadi. "
    "Yangilanishlarni kuting!"
)

# --------------------
# Button Handlers
# --------------------
@menu_router.message(F.text == "💰 Hisobim")
async def handle_balance(message: Message) -> None:
    """Show user's balance by calling backend API."""
    await send_typing(message)

    user_id = message.from_user.id  # your User.pk is Telegram user_id
    url = f"{BALANCE_ENDPOINT}/{user_id}/"

    try:
        data = await fetch_json(url)
        if not data:
            await message.answer("❗️ Balansni olishda xatolik. Keyinroq urinib ko'ring.")
            return

        # Accept both {balance_sum} or {balance}
        bal = data.get("balance_sum") if "balance_sum" in data else data.get("balance", 0)
        await message.answer(
            f"💰 Balansingiz: <b>{format_sum(bal)}</b> so'm",
            parse_mode="HTML",
            reply_markup=get_user_start_keyboard(),
        )
    except asyncio.TimeoutError:
        await message.answer("⏳ Server javobi kechikdi. Keyinroq urinib ko'ring.")
    except Exception:
        await message.answer("🚫 Serverga ulanishda xatolik yuz berdi.")


@menu_router.message(F.text == "📊 Ovoz berish")
async def handle_vote(message: Message) -> None:
    await send_typing(message, 0.3)
    await message.answer(PLACEHOLDER, reply_markup=get_user_start_keyboard())


@menu_router.message(F.text == "💸 Pul yechib olish")
async def handle_withdraw(message: Message) -> None:
    user_id = message.from_user.id
    if await has_open_request(user_id):
        await message.answer(
            "❌ Sizda hali tugallanmagan pul yechish so‘rovi bor.\n"
            "Iltimos, admin uni tasdiqlamaguncha yoki rad etmaguncha kuting.",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer("Tanlang ...", reply_markup=get_user_get_money_keyboard())







@menu_router.message(F.text == "❌ Bekor qilish")
async def handle_cancel(message: Message) -> None:
    await send_typing(message, 0.2)
    await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=get_user_start_keyboard())



