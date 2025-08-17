from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_subscribe_kb(required_rules: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for r in required_rules:
        title = r.get("title") or str(r.get("chat_id"))
        url = r.get("invite_link")
        if url:
            rows.append([InlineKeyboardButton(text=f"➕ {title}", url=url)])
    rows.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="subs_check")])
    return InlineKeyboardMarkup(inline_keyboard=rows)