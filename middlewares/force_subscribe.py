from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import aiohttp

API_BASE = "http://167.86.71.176/api/v1"

WHITELIST = { "help", "check"}

class ForceSubscribeMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]):

        user_id = event.from_user.id
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(f"{API_BASE}/api/subscribe/status/", params={"user_id": user_id}) as r:
                    payload = await r.json()
        except Exception:
            # Backend down — foydalanuvchini ushlab qolmaymiz
            return await handler(event, data)

        fully = bool(payload.get("fully_subscribed", True))
        mode = payload.get("enforcement_mode", "BLOCK")
        if fully:
            return await handler(event, data)

        # BLOCK bo'lsa, subscribe UI ko'rsatamiz va to'xtatamiz
        if mode == "BLOCK":
            from keyboards.inline.subscribe import build_subscribe_kb
            required = payload.get("required", [])
            await event.answer(
                "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling va \"/check\" bosing:",
                reply_markup=build_subscribe_kb(required)
            )
            return

        # BONUS_ONLY — ogohlantirib, davom etamiz
        from keyboards.inline.subscribe import build_subscribe_kb
        await event.answer("Bonus olish uchun quyidagi kanallarga obuna bo'ling va /check ni bosing.",
                           reply_markup=build_subscribe_kb(payload.get("required", [])))
        return await handler(event, data)