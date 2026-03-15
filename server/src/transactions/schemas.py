from pydantic import BaseModel
from typing import Optional
from src.transactions.models import TransactionType
from datetime import datetime

class TransactionBase(BaseModel):
    account_id: int
    description: str
    category: Optional[str] = None
    amount: float
    currency: str = "INR"
    txn_type: TransactionType
    merchant: Optional[str] = None
    txn_date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    description: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    txn_type: Optional[TransactionType] = None
    merchant: Optional[str] = None
    txn_date: Optional[datetime] = None

class TransactionResponse(TransactionBase):
    id: int
    posted_date: datetime

    class Config:
        from_attributes = True
