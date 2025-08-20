import asyncio
import aiohttp
from aiogram import Bot

last_id = 0  # oxirgi ko‘rilgan withdrawal id

async def poll_withdraw_updates(bot: Bot, withdraw_updates_url: str, notify_channel_id: int):
    """
    Backend API'dan PAID yoki REJECTED withdrawal'larni olib,
    userga va (PAID bo‘lsa) kanalgaham yuboradi.
    """
    global last_id
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{withdraw_updates_url}?after_id={last_id}"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for w in data:
                            last_id = w["id"]

                            status = w["status"]
                            amount = w["amount"]
                            method = w["method"]
                            dest = w["destination"]
                            user_id = w["user_id"]
                            updated_at = w["updated_at"]

                            # ---- USERGA XABAR ----
                            if status == "PAID":
                                msg_user = (
                                    "✅ <b>Pul yechish so‘rovingiz tasdiqlandi!</b>\n\n"
                                    f"💵 Summa: <b>{amount:,} so‘m</b>\n"
                                    f"💳 Usul: {method}\n"
                                    f"📍 Hisob: <code>{dest}</code>\n"
                                    f"🕒 Sana: {updated_at}\n\n"
                                    "✔️ Mablag‘ingiz hisobingizga o‘tkazildi."
                                )
                            else:  # REJECTED
                                reason = w.get("reason", "Admin rad etdi.")
                                msg_user = (
                                    "❌ <b>Pul yechish so‘rovingiz rad etildi!</b>\n\n"
                                    f"💵 Summa: <b>{amount:,} so‘m</b>\n"
                                    f"💳 Usul: {method}\n"
                                    f"📍 Hisob: <code>{dest}</code>\n"
                                    f"🕒 Sana: {updated_at}\n\n"
                                    f"📌 Sabab: <i>{reason}</i>"
                                )

                            try:
                                await bot.send_message(chat_id=user_id, text=msg_user)
                            except Exception as e:
                                print(f"Userga yuborishda xato: {e}")

                            # ---- KANALGA XABAR (faqat PAID) ----
                            if status == "PAID":
                                msg_channel = (
                                    "🎉 <b>Yangi to‘lov amalga oshirildi!</b>\n\n"
                                    f"💵 Summa: <b>{amount:,} so‘m</b>\n"
                                    f"💳 Usul: {method}\n"
                                    f"📍 Hisob: <code>{dest}</code>\n"
                                    f"🕒 Sana: {updated_at}\n\n"
                                    "🔔 Bizning xizmatimiz orqali foydalanuvchilarga to‘lovlar amalga oshirilmoqda!"
                                )
                                try:
                                    await bot.send_message(chat_id=notify_channel_id, text=msg_channel)
                                except Exception as e:
                                    print(f"Kanalga yuborishda xato: {e}")

        except Exception as e:
            print(f"Withdraw polling error: {e}")

        await asyncio.sleep(10)  # har 10 soniyada yangi update tekshirish
