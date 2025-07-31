from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime, timedelta

from infrastructure.database.models import User

import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        """Foydalanuvchini ID bo‘yicha topish."""
        try:
            result = await session.get(User, user_id)
            if result:
                logger.info(f"Foydalanuvchi topildi: {user_id}")
            else:
                logger.info(f"Foydalanuvchi topilmadi: {user_id}")
            return result
        except Exception as e:
            logger.error(f"Foydalanuvchi topishda xato: {user_id}, Xato: {e}")
            raise

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
        """Foydalanuvchini username bo‘yicha topish."""
        try:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                logger.info(f"Foydalanuvchi topildi: {username}")
            else:
                logger.info(f"Foydalanuvchi topilmadi: {username}")
            return user
        except Exception as e:
            logger.error(f"Username bo‘yicha topishda xato: {username}, Xato: {e}")
            raise

    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        """Barcha foydalanuvchilarni ro‘yxatlash."""
        try:
            query = select(User).order_by(User.created_at)
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info(f"Barcha foydalanuvchilar ro‘yxati: {len(users)} ta")
            return users
        except Exception as e:
            logger.error(f"Barcha foydalanuvchilarni olishda xato: {e}")
            raise

    @staticmethod
    async def get_daily_users(session: AsyncSession) -> List[User]:
        """Kunlik faol foydalanuvchilarni aniqlash (oxirgi 24 soat)."""
        try:
            time_threshold = datetime.utcnow() - timedelta(days=1)
            query = select(User).where(User.updated_at >= time_threshold, User.active == True)
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info(f"Kunlik faol foydalanuvchilar: {len(users)} ta")
            return users
        except Exception as e:
            logger.error(f"Kunlik foydalanuvchilarni olishda xato: {e}")
            raise

    @staticmethod
    async def get_monthly_users(session: AsyncSession) -> List[User]:
        """Oylik faol foydalanuvchilarni aniqlash (oxirgi 30 kun)."""
        try:
            time_threshold = datetime.utcnow() - timedelta(days=30)
            query = select(User).where(User.updated_at >= time_threshold, User.active == True)
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info(f"Oylik faol foydalanuvchilar: {len(users)} ta")
            return users
        except Exception as e:
            logger.error(f"Oylik foydalanuvchilarni olishda xato: {e}")
            raise

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchini o‘chirish."""
        try:
            query = delete(User).where(User.user_id == user_id)
            result = await session.execute(query)
            await session.commit()
            if result.rowcount > 0:
                logger.info(f"Foydalanuvchi o‘chirildi: {user_id}")
                return True
            logger.info(f"O‘chirish uchun foydalanuvchi topilmadi: {user_id}")
            return False
        except Exception as e:
            logger.error(f"Foydalanuvchi o‘chirishda xato: {user_id}, Xato: {e}")
            raise

    @staticmethod
    async def block_user(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchini bloklash (active=False)."""
        try:
            query = update(User).where(User.user_id == user_id).values(active=False)
            result = await session.execute(query)
            await session.commit()
            if result.rowcount > 0:
                logger.info(f"Foydalanuvchi bloklandi: {user_id}")
                return True
            logger.info(f"Bloklash uchun foydalanuvchi topilmadi: {user_id}")
            return False
        except Exception as e:
            logger.error(f"Foydalanuvchi bloklashda xato: {user_id}, Xato: {e}")
            raise

    @staticmethod
    async def unblock_user(session: AsyncSession, user_id: int) -> bool:
        """Foydalanuvchi blokdan chiqarish (active=True)."""
        try:
            query = update(User).where(User.user_id == user_id).values(active=True)
            result = await session.execute(query)
            await session.commit()
            if result.rowcount > 0:
                logger.info(f"Foydalanuvchi blokdan chiqarildi: {user_id}")
                return True
            logger.info(f"Blokdan chiqarish uchun foydalanuvchi topilmadi: {user_id}")
            return False
        except Exception as e:
            logger.error(f"Foydalanuvchi blokdan chiqarishda xato: {user_id}, Xato: {e}")
            raise