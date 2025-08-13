from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Transaction(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    type: Mapped[str] = mapped_column(String(32))
    amount_sum: Mapped[int] = mapped_column(Integer)
    ref_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
