from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import aiohttp
import re

from keyboards.default.main import get_user_start_keyboard

withdraw_router = Router(name="withdraw")

# ====== API endpoints ======
API_BASE = "http://167.86.71.176/api/v1"
API_BALANCE = f"{API_BASE}/api/balance"
API_WITHDRAW = f"{API_BASE}/withdrawals/create_request/"
API_HAS_OPEN = f"{API_BASE}/withdrawals/has_open_request/"

# Minimal withdraw
MIN_WITHDRAW = 5000


# ====== FSM states ======
class WithdrawState(StatesGroup):
    method = State()
    amount = State()
    destination = State()


# ====== Helpers ======
async def get_balance(user_id: int) -> int:
    """Backenddan balansni olib kelish"""
    url = f"{API_BALANCE}/{user_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("balance_sum", 0)
            return 0


async def has_open_request(user_id: int) -> bool:
    """Backenddan foydalanuvchida tugallanmagan so‘rov bor-yo‘qligini tekshirish"""
    url = f"{API_HAS_OPEN}?user_id={user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("has_open", False)
            return False


async def create_withdrawal(user_id: int, method: str, dest: str, amount: int):
    """Backendga withdrawal so‘rovi yuborish"""
    payload = {
        "user_id": user_id,
        "method": method,
        "destination": dest,
        "amount": amount,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_WITHDRAW, json=payload) as resp:
            return resp.status, await resp.json()


# ====== Orqaga tugma ======
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Asosiy menyu")]],
        resize_keyboard=True
    )


# ====== ENTRY POINT ======
@withdraw_router.message(F.text.in_(["💳 Paynet", "💵 UzCard / Humo"]))
async def withdraw_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    method = "PAYNET" if "Paynet" in message.text else "CARD"

    # 1) Oldingi tugallanmagan so‘rov bormi?
    if await has_open_request(user_id):
        await message.answer(
            "❌ Sizda hali tugallanmagan pul yechish so‘rovi bor.\n"
            "Iltimos, admin uni tasdiqlamaguncha yoki rad etmaguncha kuting.",
            reply_markup=main_menu_keyboard()
        )
        await state.clear()
        return

    # 2) Balansni tekshirish
    balance = await get_balance(user_id)
    if balance < MIN_WITHDRAW:
        await message.answer(
            f"❌ Sizning balansingiz: {balance:,} so‘m\n"
            f"Minimal yechish: {MIN_WITHDRAW:,} so‘m\n"
            "Balansingiz yetarli emas.",
            reply_markup=main_menu_keyboard()
        )
        await state.clear()
        return

    await state.update_data(method=method, balance=balance, user_id=user_id)

    await message.answer(
        f"✅ Balansingiz: {balance:,} so‘m\n"
        f"Minimal yechish: {MIN_WITHDRAW:,} so‘m\n\n"
        "💵 Qancha summa yechmoqchisiz yozing? \n(sonlarda kiriting, masalan: 20000)\n"
    )
    await state.set_state(WithdrawState.amount)


# ====== Step 2: Summani olish ======
@withdraw_router.message(WithdrawState.amount, F.text)
async def withdraw_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    balance = data.get("balance", 0)

    if not message.text.isdigit():
        await message.answer("❗️ Faqat son kiriting. Masalan: 20000")
        return

    amount = int(message.text)
    if amount < MIN_WITHDRAW:
        await message.answer(f"❌ Minimal summa {MIN_WITHDRAW:,} so‘m.")
        return
    if amount > balance:
        await message.answer(f"❌ Sizning balansingiz yetarli emas. (Balans: {balance:,} so‘m)")
        return

    await state.update_data(amount=amount)

    if data["method"] == "PAYNET":
        await message.answer("📱 Telefon raqamingizni kiriting: (+99890xxxxxxx)")
    else:
        await message.answer("💳 Karta raqamingizni kiriting: (16 ta raqam)")
    await state.set_state(WithdrawState.destination)


# ====== Step 3: Destination olish va withdrawal yaratish ======
@withdraw_router.message(WithdrawState.destination, F.text)
async def withdraw_destination(message: Message, state: FSMContext):
    data = await state.get_data()
    method = data["method"]
    amount = data["amount"]
    user_id = data["user_id"]
    destination = message.text.strip()

    # === Validatsiya ===
    if method == "PAYNET":
        if not re.fullmatch(r"^\+998\d{9}$", destination):
            await message.answer("❌ Telefon raqamini to‘g‘ri formatda kiriting.\nMasalan: +998901234567")
            return
    else:  # CARD
        if not re.fullmatch(r"^\d{16}$", destination):
            await message.answer("❌ Karta raqami 16 ta raqam bo‘lishi kerak.\nMasalan: 8600123412341234")
            return

    await message.answer("⏳ So‘rovingiz yuborilmoqda...")

    status, resp = await create_withdrawal(user_id, method, destination, amount)

    if status in (200, 201):
        await message.answer(
            "✅ <b>Pul yechish so‘rovingiz qabul qilindi!</b>\n\n"
            f"💳 Usul: <b>{method}</b>\n"
            f"💵 Summa: <b>{amount:,} so‘m</b>\n"
            f"📱 Hisob raqam: <code>{destination}</code>\n"
            f"📊 Holat: <b>{resp.get('status', 'PENDING')}</b>\n\n"
            "📌  So‘rovingiz admin tomonidan tekshirilgach, mablag‘ingiz tez orada o‘tkaziladi.\n"
            "ℹ️ Jarayon tugagach, sizga alohida xabar yuboriladi.",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard()
        )
    else:
        detail = resp.get("detail") if isinstance(resp, dict) else resp
        await message.answer(f"❌ Xatolik: {detail}", reply_markup=main_menu_keyboard())

    await state.clear()


# ====== Bekor qilish ======
@withdraw_router.message(F.text.in_(["❌ Bekor qilish", "/cancel"]))
async def withdraw_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=main_menu_keyboard())


@withdraw_router.message(F.text == "⬅️ Asosiy menyu")
async def back_to_main_menu(message: Message):
    """
    Foydalanuvchi '⬅️ Asosiy menyu' tugmasini bossagina ishlaydi.
    """
    await message.answer(
        "🏠 Asosiy menyuga qaytdingiz!",
        reply_markup=get_user_start_keyboard()
    )