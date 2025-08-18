from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_user_start_keyboard() -> ReplyKeyboardMarkup:
    """
    Create a simple and user-friendly start keyboard for users
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Ovoz berish"),
            ],
            [
                KeyboardButton(text="💰 Hisobim"),
                KeyboardButton(text="💸 Pul yechib olish"),
            ],
            [
                KeyboardButton(text="👥 Referal"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_user_get_money_keyboard() -> ReplyKeyboardMarkup:
    """
    Create a simple get money keyboard
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💳 Paynet"),
                KeyboardButton(text="💵 UzCard / Humo"),
            ],
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
