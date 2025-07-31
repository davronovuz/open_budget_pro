from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env

from config import DbConfig
from infrastructure.database.setup import create_session_pool, create_engine
from keyboards.inline.main import get_user_start_inline_keyboard
from infrastructure.database.models import User

user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message):
    # Konfiguratsiyani yuklash
    env = Env()
    env.read_env()
    db_config = DbConfig.from_env(env)

    # Database engine va session pool yaratish
    engine = create_engine(db_config)
    session_pool = create_session_pool(engine)

    async with session_pool() as session:
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name or "Unknown"

        # Foydalanuvchini DB dan tekshirish
        existing_user = await session.get(User, user_id)

        if not existing_user:
            new_user = User(
                user_id=user_id,
                username=username,
                full_name=full_name,
                active=True,
                language="en"
            )
            session.add(new_user)
            await session.commit()

        # Hamma foydalanuvchilar uchun xush kelibsiz xabari
        welcome_message = f"""

<b>👋 Salom {full_name}!</b>
   Ijtimoiy loyihalarga <b>ovoz berib</b> pul ishlang,  
👥 Do‘stlaringizni botga taklif qilib <b>referal bonuslar</b> oling,
💳 To‘plangan balansingizni <b>real pul</b> sifatida yechib oling.

⚠️ Har bir telefon raqam faqat <b>bitta marta</b> ovoz bera oladi.  
👇 Quyidagi tugmalardan birini tanlab, davom eting:
        """

        await message.reply(
            welcome_message,
            reply_markup=get_user_start_inline_keyboard(),
            parse_mode="HTML"
        )
