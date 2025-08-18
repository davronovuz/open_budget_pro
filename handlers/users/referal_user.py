from aiogram import Router, F
from aiogram.types import Message
import aiohttp
import os

referral_router = Router(name="referral")
API_BASE = "http://167.86.71.176/api/v1/api"
BOT_USERNAME = "openbudget_humo_bot"  # sizning bot username


async def get_reward_sum() -> int:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{API_BASE}/referral/config/", timeout=8) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("referral_reward_sum", 0)
    except Exception:
        pass
    return 0


def build_ref_link(user_id: int) -> str:
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"


@referral_router.message(F.text == "👥 Referal")
async def referral_card(message: Message):
    reward = await get_reward_sum()
    link = build_ref_link(message.from_user.id)

    text = (
        f"🔗 <b>Sizning referal havolangiz:</b> {link}\n\n"
        f"ℹ️ Do‘stingiz shu havola orqali botga kirsa, sizga <b>{reward:,}</b> so‘m mukofot tushadi."
        .replace(",", " ")
    )

    await message.answer(text, parse_mode="HTML")
    # URL preview chiqishi uchun alohida link
    await message.answer(link, disable_web_page_preview=False)


@referral_router.message(F.text == "Bekor qilish 🚫")
async def cancel(message: Message):
    await message.answer("Asosiy menyuga qaytdingiz.")
