# referral_router.py — drop-in replacement

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import aiohttp

referral_router = Router(name="referral")

API_BASE = "http://167.86.71.176/api/v1/api"      # ✅ to'g'rilandi
BOT_USERNAME = "openbudget_humo_bot"          # fixed
DEFAULT_REWARD = 5000

async def get_reward_sum() -> int:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{API_BASE}/referral/config/", timeout=8) as r:
                if r.status == 200:
                    data = await r.json()
                    return int(data.get("referral_reward_sum", DEFAULT_REWARD))
    except Exception:
        pass
    return DEFAULT_REWARD

def build_ref_link(user_id: int) -> str:
    # payload: faqat raqam (start.py shuni kutyapti)
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"

def referral_kb(link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Bekor qilish", callback_data="ref_cancel")]
    ])

@referral_router.message(F.text == "👥 Referal")
async def referral_card(message: Message):
    reward = await get_reward_sum()
    link = build_ref_link(message.from_user.id)

    text = (
        f"🔗 <b>Sizning referal havolangiz:</b> {link}\n\n"
        f"ℹ️ Do‘stingiz shu havola orqali botga kirsa, sizga <b>{reward:,}</b> so‘m mukofot tushadi."
    ).replace(",", " ")

    await message.answer(
        text, parse_mode="HTML",
        disable_web_page_preview=False,
        reply_markup=referral_kb(link)
    )

@referral_router.callback_query(F.data == "ref_cancel")
async def ref_cancel(cb: CallbackQuery):
    # faqat inline knopkalarni olib tashlaymiz (xabarning o'zi qoladi)
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await cb.answer("Bekor qilindi")
