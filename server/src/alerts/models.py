import enum
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AlertType(str, enum.Enum):
    low_balance = "low_balance"
    bill_due = "bill_due"
    budget_exceeded = "budget_exceeded"


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Alert(SQLModel, table=True):
    __tablename__ = "alerts"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    type: AlertType
    message: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class AlertCreate(SQLModel):
    type: AlertType
    message: str


class AlertRead(SQLModel):
    id: int
    user_id: int
    type: AlertType
    message: str
    created_at: datetime


class AlertUpdate(SQLModel):
    type: AlertType | None = None
    message: str | None = None
