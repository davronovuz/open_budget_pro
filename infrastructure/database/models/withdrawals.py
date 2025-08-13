from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Withdrawal(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    amount_sum: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(String(32))
    destination_masked: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), server_default=text("'PENDING'"))
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
