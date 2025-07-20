from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Time, Date, func, Text, BigInteger as BigInt
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime, date, time

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInt, unique=True, nullable=False)  # Изменено с Integer на BigInt
    language = Column(String(2), default="en")
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="user", cascade="all, delete-orphan")
    
    def is_subscription_active(self) -> bool:
        """Check if user has an active subscription"""
        if not self.is_premium:
            return False
        
        # Lifetime subscription
        if self.premium_until is None:
            return True
        
        # Subscription with expiration date
        return datetime.utcnow() < self.premium_until

class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    schedule = Column(String(20), nullable=False)  # "morning", "day", "evening", "custom"
    time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="medications")
    checklists = relationship("Checklist", back_populates="medication", cascade="all, delete-orphan")

class Checklist(Base):
    __tablename__ = "checklist"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False)
    status = Column(Boolean, default=False)  # False = not taken, True = taken
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="checklists")
    medication = relationship("Medication", back_populates="checklists")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)  # Amount in kopecks
    subscription_type = Column(String(20), nullable=False)  # "monthly", "yearly", "lifetime"
    telegram_payment_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False)  # "pending", "completed", "failed"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reminders_enabled = Column(Boolean, default=True)
    reminder_repeat_minutes = Column(Integer, default=30)  # 5, 15 или 30 минут
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="settings")
