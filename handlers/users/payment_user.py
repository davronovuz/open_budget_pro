from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import aiohttp

withdraw_router = Router(name="withdraw")

# ====== API endpoints ======
API_BASE = "http://167.86.71.176/api/v1"
API_BALANCE = f"{API_BASE}/api/balance"
API_WITHDRAW = f"{API_BASE}/api/withdrawals/create_request/"

# Minimal withdraw (server bilan sinxron qilishingiz mumkin)
MIN_WITHDRAW = 5000


# ====== FSM states ======
class WithdrawState(StatesGroup):
    method = State()
    amount = State()
    destination = State()


# ====== Helpers ======
async def get_balance(user_id: int) -> int:
    """Backenddan balansni olib kelish (telegram_id bo‘yicha)"""
    url = f"{API_BALANCE}/{user_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("balance_sum", 0)
            return 0


async def create_withdrawal(user_id: int, method: str, dest: str, amount: int):
    """Backendga withdrawal so‘rovi yuborish (telegram_id bilan)"""
    payload = {
        "user_id": user_id,          # ✅ telegram_id
        "method": method,
        "destination": dest,
        "amount": amount,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_WITHDRAW, json=payload) as resp:
            return resp.status, await resp.json()


# ====== ENTRY POINT ======
@withdraw_router.message(F.text.in_(["💳 Paynet", "💳 UzCard / Humo"]))
async def withdraw_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    method = "PAYNET" if "Paynet" in message.text else "CARD"

    balance = await get_balance(user_id)

    if balance < MIN_WITHDRAW:
        await message.answer(
            f"❌ Sizning balansingiz: {balance} so‘m\n"
            f"Minimal yechish: {MIN_WITHDRAW} so‘m\n"
            "Balansingiz yetarli emas."
        )
        await state.clear()
        return

    await state.update_data(method=method, balance=balance, user_id=user_id)

    await message.answer(
        f"✅ Balansingiz: {balance:,} so‘m\n"
        f"Minimal yechish: {MIN_WITHDRAW:,} so‘m\n\n"
        "💵 Qancha summa yechmoqchisiz?"
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

    await message.answer("⏳ So‘rovingiz yuborilmoqda...")

    status, resp = await create_withdrawal(
        user_id=user_id,
        method=method,
        dest=destination,
        amount=amount,
    )

    if status in (200, 201):
        await message.answer(
            f"✅ So‘rov qabul qilindi!\n\n"
            f"Usul: {method}\n"
            f"Summa: {amount:,} so‘m\n"
            f"Hisob: {destination}\n"
            f"Status: {resp.get('status', 'PENDING')}"
        )
    else:
        detail = resp.get("detail") if isinstance(resp, dict) else resp
        await message.answer(f"❌ Xatolik: {detail}")

    await state.clear()


# ====== Bekor qilish ======
@withdraw_router.message(F.text.in_(["❌ Bekor qilish", "/cancel"]))
async def withdraw_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.")
