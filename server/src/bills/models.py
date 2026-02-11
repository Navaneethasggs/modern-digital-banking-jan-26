import enum
from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


class BillStatus(str, enum.Enum):
    upcoming = "upcoming"
    paid = "paid"
    overdue = "overdue"


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Bill(SQLModel, table=True):
    __tablename__ = "bills"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    biller_name: str = Field(max_length=255)
    due_date: date
    amount_due: float
    status: BillStatus = Field(default=BillStatus.upcoming)
    auto_pay: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class BillCreate(SQLModel):
    biller_name: str
    due_date: date
    amount_due: float
    status: BillStatus = BillStatus.upcoming
    auto_pay: bool = False


class BillRead(SQLModel):
    id: int
    user_id: int
    biller_name: str
    due_date: date
    amount_due: float
    status: BillStatus
    auto_pay: bool
    created_at: datetime


class BillUpdate(SQLModel):
    biller_name: str | None = None
    due_date: date | None = None
    amount_due: float | None = None
    status: BillStatus | None = None
    auto_pay: bool | None = None
