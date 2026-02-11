import enum
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AccountType(str, enum.Enum):
    savings = "savings"
    checking = "checking"
    credit_card = "credit_card"
    loan = "loan"
    investment = "investment"


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    bank_name: str = Field(max_length=255)
    account_type: AccountType
    masked_account: str = Field(max_length=255)
    currency: str = Field(max_length=3)
    balance: float = Field(default=0.0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class AccountCreate(SQLModel):
    bank_name: str
    account_type: AccountType
    masked_account: str
    currency: str = "USD"
    balance: float = 0.0


class AccountRead(SQLModel):
    id: int
    user_id: int
    bank_name: str
    account_type: AccountType
    masked_account: str
    currency: str
    balance: float
    created_at: datetime


class AccountUpdate(SQLModel):
    bank_name: str | None = None
    account_type: AccountType | None = None
    masked_account: str | None = None
    currency: str | None = None
    balance: float | None = None
