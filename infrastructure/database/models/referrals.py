from sqlalchemy import Integer, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Referral(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    referrer_user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    referred_user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    bonus_sum: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    status: Mapped[str] = mapped_column(String(32), server_default=text("'PENDING'"))
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
