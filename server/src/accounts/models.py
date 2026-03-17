from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
import enum

class AccountType(str, enum.Enum):
    savings = "savings"
    checking = "checking"
    credit_card = "credit_card"
    loan = "loan"
    investment = "investment"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bank_name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    masked_account = Column(String(50), nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String(3), default="INR")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("src.auth.models.User")
