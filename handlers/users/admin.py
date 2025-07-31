from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline.main import (
    get_main_keyboard,
    get_admin_management_keyboard,
    get_channel_management_keyboard,
    get_advertisement_keyboard,
    get_project_management_keyboard,
    get_withdraw_requests_keyboard,
    get_settings_keyboard, get_statistics_keyboard,
)

admin_router = Router()

# /admin komandasi
@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("👮‍♂️ Admin paneliga xush kelibsiz!", reply_markup=get_main_keyboard())


# --- Asosiy menyudagi tugmalar ---

@admin_router.callback_query(F.data == "admins")
async def show_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text("👑 Adminlarni boshqarish menyusi:", reply_markup=get_admin_management_keyboard())


@admin_router.callback_query(F.data == "channels")
async def show_channel_menu(callback: CallbackQuery):
    await callback.message.edit_text("📡 Kanallarni boshqarish menyusi:", reply_markup=get_channel_management_keyboard())


@admin_router.callback_query(F.data == "advertisement")
async def show_advertisement_menu(callback: CallbackQuery):
    await callback.message.edit_text("📣 Reklama yuborish menyusi:", reply_markup=get_advertisement_keyboard())


@admin_router.callback_query(F.data == "project_management")
async def show_project_menu(callback: CallbackQuery):
    await callback.message.edit_text("📊 Loyihalarni boshqarish menyusi:", reply_markup=get_project_management_keyboard())


@admin_router.callback_query(F.data == "statistic")
async def show_statistics_menu(callback: CallbackQuery):
    await callback.message.edit_text("📈 Statistika bo‘limi:", reply_markup=get_statistics_keyboard())

@admin_router.callback_query(F.data == "settings")
async def show_settings_menu(callback: CallbackQuery):
    await callback.message.edit_text("⚙️ Sozlamalar menyusi:", reply_markup=get_settings_keyboard())


@admin_router.callback_query(F.data == "withdraw")
async def show_withdraw_menu(callback: CallbackQuery):
    await callback.message.edit_text("📤 Pul chiqarish so‘rovlarini boshqarish menyusi:", reply_markup=get_withdraw_requests_keyboard())


# --- Orqaga asosiy menyuga qaytish ---
@admin_router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text("🔙 Asosiy admin menyu:", reply_markup=get_main_keyboard())
