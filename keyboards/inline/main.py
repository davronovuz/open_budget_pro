from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder








# User uchun start inline keyboard
def get_user_start_inline_keyboard() -> InlineKeyboardMarkup:
    """Oddiy foydalanuvchilar uchun /start da chiqadigan inline keyboard qaytaradi."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🌟 Ovoz Berish", callback_data="vote")
    )
    builder.add(
        InlineKeyboardButton(text="💸 Balansim", callback_data="account"),
        InlineKeyboardButton(text="👥 Do'stlarni taklif qilish", callback_data="invite")
    )
    builder.add(
        InlineKeyboardButton(text="📤 Pul chiqarish", callback_data="withdraw"),
    InlineKeyboardButton(text="📄 So‘rovlarim", callback_data="my_withdraw_requests"),

    )
    builder.adjust(2)  # Har qatorga 2 ta tugma
    return builder.as_markup()



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_statistics_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="👤 Userlar statistikasi", callback_data="stat_users"),
        InlineKeyboardButton(text="🗳 Loyiha statistikasi", callback_data="stat_projects"),
    )
    builder.row(
        InlineKeyboardButton(text="🧑‍🤝‍🧑 Referal statistikasi", callback_data="stat_referrals"),
        InlineKeyboardButton(text="💵 Pul yechish statistikasi", callback_data="stat_withdraw"),
    )
    builder.row(
        InlineKeyboardButton(text="📊 Umumiy statistika", callback_data="stat_general"),
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main"),
    )

    return builder.as_markup()



def get_main_keyboard() -> InlineKeyboardMarkup:
    """
    Eng asosiy boshqaruv menyusi uchun inline tugmalar
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👑 Adminlar", callback_data="admins"),
        InlineKeyboardButton(text="📊 Loyihalar", callback_data="project_management"),
    InlineKeyboardButton(text="📡 Kanallar", callback_data="channels"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"),
        InlineKeyboardButton(text="📈 Statistika", callback_data="statistic"),
        InlineKeyboardButton(text="📣 Reklama", callback_data="advertisement")
    )
    builder.adjust(2)
    return builder.as_markup()






# Admin boshqarish menyusi uchun keyboard
def get_admin_management_keyboard() -> InlineKeyboardMarkup:
    """Adminlarni boshqarish uchun keyboard qaytaradi."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="➕ Admin qo‘shish", callback_data="add_admin"),
        InlineKeyboardButton(text="➖ Admin o‘chirish", callback_data="remove_admin"),
        InlineKeyboardButton(text="👥 Barcha adminlar", callback_data="list_admins"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()



# Kanal boshqarish menyusi uchun keyboard
def get_channel_management_keyboard() -> InlineKeyboardMarkup:
    """Kanallarni boshqarish uchun keyboard qaytaradi."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="➕ Kanal qo‘shish", callback_data="add_channel"),
        InlineKeyboardButton(text="➖ Kanal o‘chirish", callback_data="remove_channel"),
        InlineKeyboardButton(text="📋 Barcha kanallar", callback_data="list_channels"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_advertisement_keyboard() -> InlineKeyboardMarkup:
    """
    Reklama yuborishga oid sub-tugmalar: faqat reklama turlari bilan ishlash uchun.
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🖼 Matnli reklama", callback_data="ad_text"),
        InlineKeyboardButton(text="📷 Rasmli reklama", callback_data="ad_image"),
        InlineKeyboardButton(text="🎞 Videoli reklama", callback_data="ad_video"),
        InlineKeyboardButton(text="🔗 Tugmali reklama", callback_data="ad_with_button"),
        InlineKeyboardButton(text="🔁 Forward reklama yuborish", callback_data="ad_forward"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_project_management_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="➕ Loyiha qo‘shish", callback_data="add_project"),
        InlineKeyboardButton(text="🗑 Loyiha o‘chirish", callback_data="remove_project"),
        InlineKeyboardButton(text="📋 Loyiha ro‘yxati", callback_data="list_projects"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()



def get_withdraw_requests_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📥 Yangi so‘rovlar", callback_data="new_withdraw_requests"),
        InlineKeyboardButton(text="✅ Tasdiqlanganlar", callback_data="approved_requests"),
        InlineKeyboardButton(text="❌ Bekor qilinganlar", callback_data="rejected_requests"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_settings_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🎁 Referal mukofoti", callback_data="change_referral_amount"),
        InlineKeyboardButton(text="💸 Minimal pul yechish", callback_data="change_min_withdraw"),
        InlineKeyboardButton(text="💰 Ovoz berish mukofoti", callback_data="change_commission"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main")
    )
    builder.adjust(2)
    return builder.as_markup()

