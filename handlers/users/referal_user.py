# referral_router.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import aiohttp

referral_router = Router(name="referral")

API_BASE = "http://167.86.71.176/api/v1/api"      # sizning backend API
BOT_USERNAME = "openbudget_humo_bot"              # bot username
DEFAULT_REWARD = 1000

# === HELPERS ===
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


async def get_referral_stats(user_id: int) -> dict:
    url = f"{API_BASE}/referral/stats/{user_id}/"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=8) as r:
                if r.status == 200:
                    return await r.json()
    except Exception:
        pass
    return {"invited_count": 0, "paid_sum": 0}


def build_ref_link(user_id: int) -> str:
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"


def referral_kb(link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Ulashish", switch_inline_query=link)]

    ])


# === HANDLERS ===
@referral_router.message(F.text == "👥 Referal")
async def referral_card(message: Message):
    reward = await get_reward_sum()
    link = build_ref_link(message.from_user.id)
    stats = await get_referral_stats(message.from_user.id)

    text = (
        f"🔗 <b>Sizning referal havolangiz:</b>\n{link}\n\n"
        f"👥 Har bir do‘stingiz uchun: <b>{reward:,}</b> so‘m\n\n"
        f"📊 Statistika:\n"
        f"▫️ Jalb qilingan do‘stlar: <b>{stats['invited_count']}</b>\n"
        f"▫️ Umumiy mukofot: <b>{stats['paid_sum']:,}</b> so‘m"
    ).replace(",", " ")

    await message.answer(
        text, parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=referral_kb(link)
    )


@referral_router.callback_query(F.data == "ref_cancel")
async def ref_cancel(cb: CallbackQuery):
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await cb.answer("Yopildi ✅")
