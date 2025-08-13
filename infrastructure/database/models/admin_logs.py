from sqlalchemy import BIGINT, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class AdminLog(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    admin_id: Mapped[int] = mapped_column(BIGINT)
    action: Mapped[str] = mapped_column(String(128))
    payload_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
