from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from environs import Env

from config import DbConfig, load_config
from infrastructure.database.setup import create_session_pool,create_engine

from infrastructure.database.models import User



user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message):
    # .env fayldan konfiguratsiyani yuklash
    env = Env()
    env.read_env()
    db_config = DbConfig.from_env(env)  # DbConfig obyektini yaratish

    # SQLAlchemy engine va session pool yaratish
    engine = create_engine(db_config)
    session_pool = create_session_pool(engine)

    async with session_pool() as session:  # Sessiyani ochish
        # Foydalanuvchi ma'lumotlarini olish
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name or "Unknown"

        # Foydalanuvchi ma'lumotlar bazasida bor-yo‘qligini tekshirish
        existing_user = await session.get(User, user_id)
        if not existing_user:
            # Yangi foydalanuvchi qo‘shish
            new_user = User(
                user_id=user_id,
                username=username,
                full_name=full_name,
                active=True,
                language="en"
            )
            session.add(new_user)
            await session.commit()

        welcome_message = (
            "🎉 Salom, {username}! Botimizga xush kelibsiz! 😊\n"
            "Bu yerda sizga ko‘plab qiziqarli imkoniyatlar taqdim etamiz.\n"
            "🔥 Boshlash uchun /help buyrug‘ini sinab ko‘ring!"
        ).format(username=full_name)
        await message.reply(welcome_message)