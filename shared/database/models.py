from datetime import UTC, datetime

from sqlalchemy import BigInteger as BigInt
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from shared.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInt, unique=True, nullable=False)
    language = Column(String(2), default="en")
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    last_active = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="user", cascade="all, delete-orphan")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    schedule = Column(String(20), nullable=False)
    time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="medications")
    checklists = relationship(
        "Checklist", back_populates="medication", cascade="all, delete-orphan"
    )


class Checklist(Base):
    __tablename__ = "checklist"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "medication_id", "date", name="uq_checklist_user_medication_date"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    medication_id = Column(
        Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(Boolean, default=False)
    reminder_sent_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    user = relationship("User", back_populates="checklists")
    medication = relationship("Medication", back_populates="checklists")


class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(BigInt, nullable=False)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    replaced_by = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)

    user = relationship("User", backref="refresh_tokens")


class NotificationOutbox(Base):
    __tablename__ = "notifications_outbox"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('reminder', 'followup')",
            name="ck_notifications_outbox_kind",
        ),
        CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'dead')",
            name="ck_notifications_outbox_status",
        ),
    )

    id = Column(
        BigInt().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    medication_id = Column(
        Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False
    )
    checklist_id = Column(Integer, ForeignKey("checklist.id", ondelete="CASCADE"), nullable=False)
    kind = Column(String(16), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(16), nullable=False, default="pending")
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reminders_enabled = Column(Boolean, default=True)
    reminder_repeat_minutes = Column(Integer, default=30)
    timezone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    user = relationship("User", backref="settings")
