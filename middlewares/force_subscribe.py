from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import aiohttp

API_BASE = "http://167.86.71.176/api/v1"

WHITELIST = {"help", "check"}  # faqat shu komandalar uchun tekshirmaymiz


class ForceSubscribeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):
        # faqat Message event uchun ishlatamiz
        if not isinstance(event, Message):
            return await handler(event, data)

        # Agar komandasi whitelist ichida bo‘lsa → tekshirmaymiz
        if event.text:
            cmd = event.text.lstrip("/").split()[0].lower()
            if cmd in WHITELIST:
                return await handler(event, data)

        user_id = event.from_user.id
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    f"{API_BASE}/api/subscribe/status/",
                    params={"user_id": user_id}
                ) as r:
                    payload = await r.json()
        except Exception:
            # backend ishlamasa — bloklamaymiz
            return await handler(event, data)

        fully = bool(payload.get("fully_subscribed", True))
        mode = payload.get("enforcement_mode", "BLOCK")

        if fully:
            return await handler(event, data)

        from keyboards.inline.subscribe import build_subscribe_kb

        if mode == "BLOCK":
            await event.answer(
                "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling va /check yuboring:",
                reply_markup=build_subscribe_kb(payload.get("required", [])),
            )
            return

        # BONUS_ONLY rejimi
        await event.answer(
            "Bonus olish uchun quyidagi kanallarga obuna bo‘ling va /check yuboring.",
            reply_markup=build_subscribe_kb(payload.get("required", [])),
        )
        return await handler(event, data)
