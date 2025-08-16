from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Optional

from infrastructure.database.models.users import WithdrawStatus


# ===== USER KEYBOARDS =====

def get_user_start_inline_keyboard() -> InlineKeyboardMarkup:
    """Oddiy foydalanuvchilar uchun /start da chiqadigan inline keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🗳 Ovoz Berish", callback_data="vote"),
        InlineKeyboardButton(text="💰 Balansim", callback_data="account")
    )
    builder.row(
        InlineKeyboardButton(text="👥 Do'stlarni taklif qilish", callback_data="invite"),
        InlineKeyboardButton(text="📤 Pul chiqarish", callback_data="withdraw")
    )
    builder.row(
        InlineKeyboardButton(text="📄 So'rovlarim", callback_data="my_withdraw_requests"),
        InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")
    )
    builder.row(
        InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="user_settings")
    )
    return builder.as_markup()


def get_vote_projects_keyboard(projects: List[dict], page: int = 0, per_page: int = 5) -> InlineKeyboardMarkup:
    """Ovoz berish uchun loyihalar ro'yxati."""
    builder = InlineKeyboardBuilder()

    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_projects = projects[start_idx:end_idx]

    for project in page_projects:
        builder.row(
            InlineKeyboardButton(
                text=f"🏘 {project['title'][:30]}..." if len(project['title']) > 30 else f"🏘 {project['title']}",
                callback_data=f"vote_project_{project['id']}"
            )
        )

    # Pagination tugmalari
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"vote_page_{page - 1}"))

    total_pages = (len(projects) + per_page - 1) // per_page
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"vote_page_{page + 1}"))

    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user"))
    return builder.as_markup()


def get_vote_confirmation_keyboard(project_id: int) -> InlineKeyboardMarkup:
    """Ovoz berishni tasdiqlash keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ovoz berish", callback_data=f"confirm_vote_{project_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="vote")
    )
    return builder.as_markup()


def get_withdraw_methods_keyboard() -> InlineKeyboardMarkup:
    """Pul yechish usullari."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Bank kartasi", callback_data="withdraw_card"),
        InlineKeyboardButton(text="📱 Telefon raqami", callback_data="withdraw_phone")
    )
    builder.row(
        InlineKeyboardButton(text="🏦 Bank hisobi", callback_data="withdraw_bank"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_phone_verification_keyboard(project_id: int) -> InlineKeyboardMarkup:
    """Telefon raqam tasdiqlash keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Kodni qayta yuborish", callback_data=f"resend_code_{project_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="vote")
    )
    return builder.as_markup()


def get_vote_success_keyboard(project_id: int, reward_amount: int) -> InlineKeyboardMarkup:
    """Muvaffaqiyatli ovoz berish keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🗳 Boshqa loyihaga ovoz berish", callback_data="vote"),
        InlineKeyboardButton(text="💰 Balansimni ko'rish", callback_data="account")
    )
    builder.row(
        InlineKeyboardButton(text="👥 Do'stlarni taklif qilish", callback_data="invite"),
        InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_account_keyboard(balance: int) -> InlineKeyboardMarkup:
    """Foydalanuvchi hisobi keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📤 Pul chiqarish", callback_data="withdraw"),
        InlineKeyboardButton(text="📊 Tranzaksiyalar tarixi", callback_data="transaction_history")
    )
    builder.row(
        InlineKeyboardButton(text="🗳 Ovozlarim", callback_data="my_votes"),
        InlineKeyboardButton(text="👥 Taklif etganlarim", callback_data="my_referrals")
    )
    builder.row(
        InlineKeyboardButton(text="📄 Pul yechish so'rovlarim", callback_data="my_withdraw_requests"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_referral_keyboard(referral_code: str) -> InlineKeyboardMarkup:
    """Referral tizimi keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📋 Linkni nusxalash", callback_data=f"copy_referral_{referral_code}")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Taklif statistikam", callback_data="my_referral_stats"),
        InlineKeyboardButton(text="👥 Taklif etganlarim", callback_data="my_referrals")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_withdrawal_amount_keyboard() -> InlineKeyboardMarkup:
    """Pul yechish miqdori keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="50,000", callback_data="withdraw_amount_50000"),
        InlineKeyboardButton(text="100,000", callback_data="withdraw_amount_100000")
    )
    builder.row(
        InlineKeyboardButton(text="200,000", callback_data="withdraw_amount_200000"),
        InlineKeyboardButton(text="500,000", callback_data="withdraw_amount_500000")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Butun balansni", callback_data="withdraw_all"),
        InlineKeyboardButton(text="✏️ Boshqa miqdor", callback_data="withdraw_custom_amount")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Yordam keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❓ Tez-tez so'raladigan savollar", callback_data="faq"),
        InlineKeyboardButton(text="📞 Qo'llab-quvvatlash", callback_data="support")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Qo'llanma", callback_data="manual"),
        InlineKeyboardButton(text="🎯 Bot haqida", callback_data="about_bot")
    )
    builder.row(
        InlineKeyboardButton(text="📨 Admin bilan bog'lanish", callback_data="contact_admin"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_user_settings_keyboard() -> InlineKeyboardMarkup:
    """Foydalanuvchi sozlamalari keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🌐 Til o'zgartirish", callback_data="change_language"),
        InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="notification_settings")
    )
    builder.row(
        InlineKeyboardButton(text="🔐 Maxfiylik", callback_data="privacy_settings"),
        InlineKeyboardButton(text="📱 Telefon raqam", callback_data="change_phone")
    )
    builder.row(
        InlineKeyboardButton(text="🗑 Hisobni o'chirish", callback_data="delete_account"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_user")
    )
    return builder.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
    )
    builder.row(
        InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="user_settings")
    )
    return builder.as_markup()


# ===== ADMIN KEYBOARDS =====

def get_main_admin_keyboard() -> InlineKeyboardMarkup:
    """Asosiy admin boshqaruv menyusi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🗳 Loyihalar", callback_data="project_management"),
        InlineKeyboardButton(text="👤 Foydalanuvchilar", callback_data="user_management")
    )
    builder.row(
        InlineKeyboardButton(text="💸 Pul yechish", callback_data="withdraw_management"),
        InlineKeyboardButton(text="👑 Adminlar", callback_data="admin_management")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="statistics"),
        InlineKeyboardButton(text="📣 Reklama", callback_data="advertisement")
    )
    builder.row(
        InlineKeyboardButton(text="📡 Kanallar", callback_data="channel_management"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
    )
    builder.row(
        InlineKeyboardButton(text="📝 Loglar", callback_data="logs"),
        InlineKeyboardButton(text="🔧 Texnik", callback_data="technical")
    )
    return builder.as_markup()


# ===== PROJECT MANAGEMENT KEYBOARDS =====

def get_project_management_keyboard() -> InlineKeyboardMarkup:
    """Loyihalarni boshqarish asosiy menyusi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Loyiha qo'shish", callback_data="add_project"),
        InlineKeyboardButton(text="📋 Loyihalar ro'yxati", callback_data="list_projects")
    )
    builder.row(
        InlineKeyboardButton(text="✏️ Loyiha tahrirlash", callback_data="edit_project"),
        InlineKeyboardButton(text="🗑 Loyiha o'chirish", callback_data="delete_project")
    )
    builder.row(
        InlineKeyboardButton(text="▶️ Loyihani faollashtirish", callback_data="activate_project"),
        InlineKeyboardButton(text="⏸ Loyihani to'xtatish", callback_data="deactivate_project")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Loyiha statistikasi", callback_data="project_stats"),
        InlineKeyboardButton(text="🔄 Ma'lumotlarni yangilash", callback_data="refresh_projects")
    )
    builder.row(
        InlineKeyboardButton(text="📤 Loyihalarni eksport", callback_data="export_projects"),
        InlineKeyboardButton(text="📥 Loyihalarni import", callback_data="import_projects")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
    )
    return builder.as_markup()


def get_project_list_keyboard(projects: List[dict], page: int = 0, per_page: int = 8) -> InlineKeyboardMarkup:
    """Loyihalar ro'yxati keyboard."""
    builder = InlineKeyboardBuilder()

    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_projects = projects[start_idx:end_idx]

    for project in page_projects:
        status_emoji = "✅" if project['is_active'] else "❌"
        votes_count = project.get('votes_count', 0)
        builder.row(
            InlineKeyboardButton(
                text=f"{status_emoji} {project['title'][:25]}... ({votes_count} ovoz)",
                callback_data=f"view_project_{project['id']}"
            )
        )

    # Pagination
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"projects_page_{page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"📄 {page + 1}", callback_data="current_page"))

    total_pages = (len(projects) + per_page - 1) // per_page
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"projects_page_{page + 1}"))

    if len(nav_buttons) > 1:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_projects"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="project_management")
    )
    return builder.as_markup()


def get_project_detail_keyboard(project_id: int, is_active: bool) -> InlineKeyboardMarkup:
    """Bitta loyiha tafsilotlari keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"edit_project_{project_id}"),
        InlineKeyboardButton(text="📊 Statistika", callback_data=f"project_stats_{project_id}")
    )

    # Faollik holati
    if is_active:
        builder.row(
            InlineKeyboardButton(text="⏸ To'xtatish", callback_data=f"deactivate_project_{project_id}")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="▶️ Faollashtirish", callback_data=f"activate_project_{project_id}")
        )

    builder.row(
        InlineKeyboardButton(text="🗳 Ovozlarni ko'rish", callback_data=f"view_votes_{project_id}"),
        InlineKeyboardButton(text="🔗 Linkni test qilish", callback_data=f"test_link_{project_id}")
    )

    builder.row(
        InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delete_project_confirm_{project_id}"),
        InlineKeyboardButton(text="📋 Nusxalash", callback_data=f"duplicate_project_{project_id}")
    )

    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="list_projects")
    )
    return builder.as_markup()


def get_project_edit_keyboard(project_id: int) -> InlineKeyboardMarkup:
    """Loyiha tahrirlash keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📝 Sarlavha", callback_data=f"edit_title_{project_id}"),
        InlineKeyboardButton(text="📄 Tavsif", callback_data=f"edit_description_{project_id}")
    )
    builder.row(
        InlineKeyboardButton(text="📍 Hudud", callback_data=f"edit_region_{project_id}"),
        InlineKeyboardButton(text="🏘 Tuman", callback_data=f"edit_district_{project_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔗 Link", callback_data=f"edit_url_{project_id}"),
        InlineKeyboardButton(text="💰 Mukofot", callback_data=f"edit_reward_{project_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔢 Ovoz limiti", callback_data=f"edit_limit_{project_id}"),
        InlineKeyboardButton(text="📅 Vaqt oralig'i", callback_data=f"edit_dates_{project_id}")
    )
    builder.row(
        InlineKeyboardButton(text="✅ Saqlash", callback_data=f"save_project_{project_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"view_project_{project_id}")
    )
    return builder.as_markup()


def get_project_confirmation_keyboard(action: str, project_id: int) -> InlineKeyboardMarkup:
    """Loyiha amallarini tasdiqlash keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ha, tasdiqlash", callback_data=f"confirm_{action}_{project_id}"),
        InlineKeyboardButton(text="❌ Yo'q, bekor qilish", callback_data=f"view_project_{project_id}")
    )
    return builder.as_markup()


# ===== USER MANAGEMENT KEYBOARDS =====

def get_user_management_keyboard() -> InlineKeyboardMarkup:
    """Foydalanuvchilarni boshqarish."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👥 Barcha foydalanuvchilar", callback_data="list_users"),
        InlineKeyboardButton(text="🔍 Foydalanuvchi qidirish", callback_data="search_user")
    )
    builder.row(
        InlineKeyboardButton(text="🚫 Bloklangan foydalanuvchilar", callback_data="blocked_users"),
        InlineKeyboardButton(text="⭐ Faol foydalanuvchilar", callback_data="active_users")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Balans bo'yicha", callback_data="users_by_balance"),
        InlineKeyboardButton(text="🗳 Ovozlar bo'yicha", callback_data="users_by_votes")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Foydalanuvchi statistikasi", callback_data="user_stats"),
        InlineKeyboardButton(text="📤 Eksport", callback_data="export_users")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
    )
    return builder.as_markup()


def get_user_detail_keyboard(user_id: int, is_blocked: bool = False) -> InlineKeyboardMarkup:
    """Foydalanuvchi tafsilotlari keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📊 To'liq ma'lumot", callback_data=f"user_full_info_{user_id}"),
        InlineKeyboardButton(text="🗳 Ovozlar tarixi", callback_data=f"user_votes_{user_id}")
    )

    builder.row(
        InlineKeyboardButton(text="💰 Balans tarixi", callback_data=f"user_transactions_{user_id}"),
        InlineKeyboardButton(text="📤 Pul yechish tarihi", callback_data=f"user_withdrawals_{user_id}")
    )

    # Block/Unblock
    if is_blocked:
        builder.row(
            InlineKeyboardButton(text="✅ Blokdan chiqarish", callback_data=f"unblock_user_{user_id}")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="🚫 Bloklash", callback_data=f"block_user_{user_id}")
        )

    builder.row(
        InlineKeyboardButton(text="💸 Balansni o'zgartirish", callback_data=f"adjust_balance_{user_id}"),
        InlineKeyboardButton(text="📨 Xabar yuborish", callback_data=f"message_user_{user_id}")
    )

    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="list_users")
    )
    return builder.as_markup()


# ===== WITHDRAW MANAGEMENT KEYBOARDS =====

def get_withdraw_management_keyboard() -> InlineKeyboardMarkup:
    """Pul yechish boshqaruvi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📥 Yangi so'rovlar", callback_data="pending_withdrawals"),
        InlineKeyboardButton(text="⏳ Jarayonda", callback_data="processing_withdrawals")
    )
    builder.row(
        InlineKeyboardButton(text="✅ Tasdiqlanganlar", callback_data="approved_withdrawals"),
        InlineKeyboardButton(text="❌ Rad etilganlar", callback_data="rejected_withdrawals")
    )
    builder.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="withdrawal_stats"),
        InlineKeyboardButton(text="📤 Eksport", callback_data="export_withdrawals")
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="withdrawal_settings"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
    )
    return builder.as_markup()


def get_withdraw_detail_keyboard(withdraw_id: int, status: str) -> InlineKeyboardMarkup:
    """💰 Pul yechish so'rovi tafsilotlari uchun interaktiv keyboard"""
    builder = InlineKeyboardBuilder()

    # Holatiga qarab amallar
    if status == WithdrawStatus.PENDING.value:
        builder.row(
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_withdraw_{withdraw_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_withdraw_{withdraw_id}")
        )
        builder.row(
            InlineKeyboardButton(text="⏳ Jarayonga o'tkazish", callback_data=f"process_withdraw_{withdraw_id}"),
            InlineKeyboardButton(text="📞 Foydalanuvchiga murojaat", callback_data=f"contact_user_{withdraw_id}")
        )

    elif status == WithdrawStatus.PROCESSING.value:
        builder.row(
            InlineKeyboardButton(text="✅ Tugatish", callback_data=f"complete_withdraw_{withdraw_id}"),
            InlineKeyboardButton(text="⏸ To'xtatish", callback_data=f"pause_withdraw_{withdraw_id}")
        )

    elif status == WithdrawStatus.APPROVED.value:
        builder.row(
            InlineKeyboardButton(text="📋 Chekni ko'rish", callback_data=f"view_receipt_{withdraw_id}"),
            InlineKeyboardButton(text="🔄 Qayta ishlash", callback_data=f"reprocess_withdraw_{withdraw_id}")
        )

    # Umumiy tugmalar
    builder.row(
        InlineKeyboardButton(text="👤 Foydalanuvchi profili", callback_data=f"user_profile_from_withdraw_{withdraw_id}"),
        InlineKeyboardButton(text="📊 To'lov tarixi", callback_data=f"payment_history_{withdraw_id}")
    )

    builder.row(
        InlineKeyboardButton(text="📝 Izoh qo'shish", callback_data=f"add_withdraw_note_{withdraw_id}"),
        InlineKeyboardButton(text="🔄 Holatni yangilash", callback_data=f"update_withdraw_status_{withdraw_id}")
    )

    # Orqaga tugmasi
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="withdraw_management")
    )

    return builder.as_markup()


# ===== ADMIN MANAGEMENT KEYBOARDS =====

def get_admin_management_keyboard() -> InlineKeyboardMarkup:
    """Adminlarni boshqarish uchun keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"),
        InlineKeyboardButton(text="➖ Admin o'chirish", callback_data="remove_admin")
    )
    builder.row(
        InlineKeyboardButton(text="👥 Barcha adminlar", callback_data="list_admins"),
        InlineKeyboardButton(text="📊 Admin faolligi", callback_data="admin_activity")
    )
    builder.row(
        InlineKeyboardButton(text="🔐 Ruxsatlar", callback_data="admin_permissions"),
        InlineKeyboardButton(text="📝 Admin loglari", callback_data="admin_logs")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
    )
    return builder.as_markup()


def get_admin_permissions_keyboard(admin_id: int) -> InlineKeyboardMarkup:
    """Admin ruxsatlari keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🗳 Loyihalar", callback_data=f"toggle_perm_projects_{admin_id}"),
        InlineKeyboardButton(text="👤 Foydalanuvchilar", callback_data=f"toggle_perm_users_{admin_id}")
    )
    builder.row(
        InlineKeyboardButton(text="💸 Pul yechish", callback_data=f"toggle_perm_withdrawals_{admin_id}"),
        InlineKeyboardButton(text="📊 Statistika", callback_data=f"toggle_perm_stats_{admin_id}")
    )
    builder.row(
        InlineKeyboardButton(text="📣 Reklama", callback_data=f"toggle_perm_ads_{admin_id}"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data=f"toggle_perm_settings_{admin_id}")
    )
    builder.row(
        InlineKeyboardButton(text="✅ Saqlash", callback_data=f"save_permissions_{admin_id}"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="list_admins")
    )
    return builder.as_markup()


# ===== CHANNEL MANAGEMENT KEYBOARDS =====

def get_channel_management_keyboard() -> InlineKeyboardMarkup:
    """Kanallarni boshqarish uchun keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"),
        InlineKeyboardButton(text="➖ Kanal o'chirish", callback_data="remove_channel")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Barcha kanallar", callback_data="list_channels"),
        InlineKeyboardButton(text="🔄 Kanallarni tekshirish", callback_data="check_channels")
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Kanal sozlamalari", callback_data="channel_settings"),
        InlineKeyboardButton(text="📊 Kanal statistikasi", callback_data="channel_stats")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
    )
    return builder.as_markup()


