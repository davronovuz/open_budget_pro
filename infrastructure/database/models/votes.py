from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Vote(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    phone_snapshot: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), server_default=text("'PENDING'"))
    attempt_count: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    proof_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ob_vote_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint('project_id', 'phone_snapshot', name='uq_project_phone'),
    )
