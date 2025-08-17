from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import aiohttp
from keyboards.inline.subscribe import build_subscribe_kb

API_BASE = "http://167.86.71.176/api/v1"
BOT_SECRET = "super-strong-random-secret-key"


subscribe_router = Router()

@subscribe_router.message(F.text == "/check")
async def cmd_check(msg: Message):
    user_id = msg.from_user.id

    # 1) Active required ro'yxatni olamiz
    async with aiohttp.ClientSession() as sess:
        async with sess.get(f"{API_BASE}/api/required-channels/") as r:
            required_payload = await r.json()
    required = required_payload.get("required", [])

    # 2) Har biri bo'yicha getChatMember → snapshot_update
    for rc in required:
        chat_id = rc.get("chat_id")
        channel_id = rc.get("id")  # RequiredChannel.id
        is_member = False
        meta_err = None
        try:
            member = await msg.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            is_member = member.status in {"creator", "administrator", "member"}
        except Exception as e:
            meta_err = str(e)
        async with aiohttp.ClientSession() as sess:
            await sess.post(f"{API_BASE}/api/subscriptions/snapshot/",
                            headers={"X-Bot-Secret": BOT_SECRET},
                            json={"user_id": user_id, "channel_id": channel_id, "is_member": is_member, "error": meta_err})

    # 3) Yakuniy holat
    async with aiohttp.ClientSession() as sess:
        async with sess.get(f"{API_BASE}/api/subscribe/status/", params={"user_id": user_id}) as r2:
            status_payload = await r2.json()

    if status_payload.get("fully_subscribed"):
        await msg.answer("✅ Rahmat! Endi bot funksiyalaridan to'liq foydalana olasiz.")
    else:
        await msg.answer("❗️ Hali barcha majburiy kanallarga a'zo emassiz. Quyidagi tugmalar orqali obuna bo'ling va /check ni qayta bosing.",
                         reply_markup=build_subscribe_kb(status_payload.get("required", [])))

@subscribe_router.callback_query(F.data == "subs_check")
async def cb_check(c: CallbackQuery):
    # callback tugmasi orqali ham /check oqimini qayta chaqiramiz
    await cmd_check(c.message)
    await c.answer()