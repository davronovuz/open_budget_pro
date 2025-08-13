from sqlalchemy import JSON, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class SeleniumJob(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    vote_id: Mapped[int] = mapped_column(ForeignKey('votes.id', ondelete='CASCADE'))
    status: Mapped[str] = mapped_column(String(32), server_default=text("'QUEUED'"))
    node: Mapped[str | None] = mapped_column(String(64), nullable=True)
    timings: Mapped[dict | None] = mapped_column(JSON, nullable=True)
