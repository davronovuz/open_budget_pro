from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_projects_keyboard(projects) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for project in projects:
        builder.button(text=project.title, callback_data=f"project:{project.id}")
    builder.button(text="⬅️ Bosh menyu", callback_data="back_to_home")
    builder.adjust(1)
    return builder.as_markup()


def get_back_to_home_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Bosh menyu", callback_data="back_to_home")
    return builder.as_markup()
