import enum
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class TxnType(str, enum.Enum):
    debit = "debit"
    credit = "credit"


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    description: str = Field(max_length=500)
    category: str = Field(max_length=255)
    amount: float
    currency: str = Field(max_length=3)
    txn_type: TxnType
    merchant: str = Field(max_length=255)
    txn_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    posted_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class TransactionCreate(SQLModel):
    account_id: int
    description: str
    category: str
    amount: float
    currency: str = "USD"
    txn_type: TxnType
    merchant: str
    txn_date: datetime | None = None
    posted_date: datetime | None = None


class TransactionRead(SQLModel):
    id: int
    account_id: int
    description: str
    category: str
    amount: float
    currency: str
    txn_type: TxnType
    merchant: str
    txn_date: datetime
    posted_date: datetime


class TransactionUpdate(SQLModel):
    description: str | None = None
    category: str | None = None
    amount: float | None = None
    currency: str | None = None
    txn_type: TxnType | None = None
    merchant: str | None = None
    txn_date: datetime | None = None
    posted_date: datetime | None = None
