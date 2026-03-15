from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
import enum

class TransactionType(str, enum.Enum):
    debit = "debit"
    credit = "credit"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    description = Column(String(255), nullable=False)
    category = Column(String(100))
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    txn_type = Column(Enum(TransactionType), nullable=False)
    merchant = Column(String, nullable=True)
    txn_date = Column(DateTime(timezone=True), default=func.now())
    posted_date = Column(DateTime(timezone=True), default=func.now())

    account = relationship("src.accounts.models.Account")
