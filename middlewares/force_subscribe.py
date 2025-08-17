# middlewares/force_subscribe.py
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Optional
import aiohttp
import logging

API_BASE = "http://167.86.71.176/api/v1"
WHITELIST = {"help", "check"}  # bu komandalar tekshiruvsiz o‘tadi


def extract_command(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    # "/cmd arg1 arg2" -> "cmd"
    return text.lstrip("/").split()[0].lower()


class ForceSubscribeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ):
        # 1) Event turini ajratamiz
        message: Optional[Message] = None
        if isinstance(event, Message):
            message = event
        elif isinstance(event, CallbackQuery):
            message = event.message  # callbackdan kelgan message
        else:
            # boshqa eventlar (my_chat_member, poll...) – tekshiruvsiz o‘tkazamiz
            return await handler(event, data)

        if not message or not message.from_user:
            return await handler(event, data)

        user_id = message.from_user.id

        # 2) WHITELIST (faqat komandalar uchun)
        # Faqat Message bo‘lsa va komandaga o‘xshasa tekshiramiz
        cmd = extract_command(message.text) if isinstance(event, Message) else None
        if cmd in WHITELIST:
            return await handler(event, data)

        # 3) Backend orqali subscribe holatini tekshirish
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    f"{API_BASE}/api/subscribe/status/",
                    params={"user_id": user_id},
                    timeout=8
                ) as r:
                    payload = await r.json()
        except Exception as e:
            logging.warning("Subscribe check skipped (API error): %s", e)
            return await handler(event, data)

        fully = bool(payload.get("fully_subscribed", True))
        mode = payload.get("enforcement_mode", "BLOCK")
        required = payload.get("required", [])

        if fully:
            return await handler(event, data)

        # 4) Bloklash/ogohlantirish
        from keyboards.inline.subscribe import build_subscribe_kb
        text_block = (
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling va /check yuboring:"
            if mode == "BLOCK"
            else "Bonus olish uchun quyidagi kanallarga obuna bo‘ling va /check yuboring."
        )

        # Callback yoki Message – qaysi biri bo‘lsa o‘shanga javob
        if isinstance(event, CallbackQuery):
            # callbackga javob beramiz, so‘ngra chatga xabar qoldiramiz (yaxshi UX)
            try:
                await event.answer("Obuna talab qilinadi", show_alert=False)
            except Exception:
                pass
            await message.answer(text_block, reply_markup=build_subscribe_kb(required))
            return  # bloklaymiz
        else:
            await message.answer(text_block, reply_markup=build_subscribe_kb(required))
            return  # bloklaymiz
