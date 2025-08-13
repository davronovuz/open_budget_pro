from sqlalchemy import Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Project(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    ob_project_id: Mapped[str] = mapped_column(String(64), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    reward_sum: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    target_votes: Mapped[int | None] = mapped_column(Integer, nullable=True)
