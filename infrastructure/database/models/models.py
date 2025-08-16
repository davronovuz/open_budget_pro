from __future__ import annotations
import enum
from datetime import datetime
from typing import Optional, Annotated

from sqlalchemy import (
    BIGINT, Boolean, ForeignKey, Integer, String, JSON, TIMESTAMP, text, true,
    Index, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

# Helpers
int_pk = Annotated[int, mapped_column(primary_key=True)]

# Base
class Base(DeclarativeBase):
    pass

# Mixins
class TableNameMixin:
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

# Enums
class VoteStatus(str, enum.Enum):
    PENDING = "PENDING"
    OTP_REQUIRED = "OTP_REQUIRED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

class SeleniumJobStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"

class ReferralStatus(str, enum.Enum):
    PENDING = "PENDING"
    QUALIFIED = "QUALIFIED"
    PAID = "PAID"
    REJECTED = "REJECTED"

class TransactionType(str, enum.Enum):
    REWARD = "REWARD"
    REFERRAL = "REFERRAL"
    WITHDRAWAL = "WITHDRAWAL"
    ADJUSTMENT = "ADJUSTMENT"
    PENALTY = "PENALTY"

class WithdrawalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PAID = "PAID"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"

class WithdrawalMethod(str, enum.Enum):
    CARD = "CARD"
    CLICK = "CLICK"
    PAYME = "PAYME"
    OTHER = "OTHER"

class ChannelType(str, enum.Enum):
    PAYOUTS = "PAYOUTS"
    ALERTS = "ALERTS"

# Models
class User(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())
    language: Mapped[str] = mapped_column(String(10), server_default=text("'uz'"))
    balance_sum: Mapped[int] = mapped_column(Integer, default=0)
    phones: Mapped[list["UserPhone"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class UserPhone(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "userphones"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    phone_e164: Mapped[str] = mapped_column(String(24))
    phone_snapshot: Mapped[str] = mapped_column(String(24))
    user: Mapped["User"] = relationship(back_populates="phones")
    __table_args__ = (
        Index("uq_user_phone_per_user", "user_id", "phone_e164", unique=True),
        Index("ix_userphone_snapshot", "phone_snapshot"),
    )

class Project(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    ob_project_id: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(1024))
    region: Mapped[Optional[str]] = mapped_column(String(128))
    district: Mapped[Optional[str]] = mapped_column(String(128))
    category: Mapped[Optional[str]] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    reward_sum: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    target_votes: Mapped[Optional[int]] = mapped_column(Integer)

class Vote(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "votes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    user_phone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("userphones.id", ondelete="SET NULL"))
    phone_snapshot: Mapped[str] = mapped_column(String(24))
    status: Mapped[VoteStatus] = mapped_column(String(24), default=VoteStatus.PENDING.value)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    selenium_session_id: Mapped[Optional[str]] = mapped_column(String(128))
    ob_vote_id: Mapped[Optional[str]] = mapped_column(String(64))
    proof_screenshot_path: Mapped[Optional[str]] = mapped_column(String(1024))
    error_message: Mapped[Optional[str]] = mapped_column(String(512))
    __table_args__ = (
        UniqueConstraint("project_id", "phone_snapshot", name="uq_vote_phone_per_project"),
        UniqueConstraint("project_id", "user_phone_id", name="uq_vote_userphone_per_project"),
        Index("ix_votes_project_status", "project_id", "status"),
        Index("ix_votes_user", "user_id"),
    )

class OtpAttempt(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "otpattempts"
    id: Mapped[int_pk]
    vote_id: Mapped[int] = mapped_column(ForeignKey("votes.id", ondelete="CASCADE"))
    code_entered: Mapped[str] = mapped_column(String(16))
    result: Mapped[str] = mapped_column(String(16))

class Referral(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "referrals"
    id: Mapped[int_pk]
    referrer_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    referred_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    bonus_sum: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    status: Mapped[str] = mapped_column(String(16), server_default=text("'PENDING'"))
    reason: Mapped[Optional[str]] = mapped_column(String(255))

class Transaction(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "transactions"
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(16))
    amount_sum: Mapped[int] = mapped_column(Integer)
    ref_id: Mapped[Optional[int]] = mapped_column(Integer)

class Withdrawal(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "withdrawals"
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    amount_sum: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(String(16))
    destination_masked: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(16), server_default=text("'PENDING'"))
    admin_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    admin_note: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class AdminLog(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "adminlogs"
    id: Mapped[int_pk]
    admin_id: Mapped[int] = mapped_column(BIGINT)
    action: Mapped[str] = mapped_column(String(128))
    payload_json: Mapped[Optional[dict]] = mapped_column(JSON)

class SeleniumJob(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "seleniumjobs"
    id: Mapped[int_pk]
    vote_id: Mapped[int] = mapped_column(ForeignKey("votes.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(16), server_default=text("'QUEUED'"))
    node: Mapped[Optional[str]] = mapped_column(String(64))
    timings: Mapped[Optional[dict]] = mapped_column(JSON)
    error: Mapped[Optional[str]] = mapped_column(String(255))

class Channel(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "channels"
    id: Mapped[int_pk]
    chat_id: Mapped[int] = mapped_column(BIGINT)
    type: Mapped[str] = mapped_column(String(16))
    title: Mapped[Optional[str]] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

class Setting(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "settings"
    id: Mapped[int_pk]
    key: Mapped[str] = mapped_column(String(64), unique=True)
    active_project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    default_reward_sum: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    allow_multiple_active_projects: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

class ExportJob(Base, TimestampMixin, TableNameMixin):
    __tablename__ = "exportjobs"
    id: Mapped[int_pk]
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(16), default="PENDING")
    params: Mapped[Optional[dict]] = mapped_column(JSON)
    file_path: Mapped[Optional[str]] = mapped_column(String(1024))
    error: Mapped[Optional[str]] = mapped_column(String(255))
