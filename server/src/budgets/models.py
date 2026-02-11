from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Budget(SQLModel, table=True):
    __tablename__ = "budgets"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    month: int
    year: int
    category: str = Field(max_length=255)
    limit_amount: float
    spent_amount: float = Field(default=0.0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class BudgetCreate(SQLModel):
    month: int
    year: int
    category: str
    limit_amount: float
    spent_amount: float = 0.0


class BudgetRead(SQLModel):
    id: int
    user_id: int
    month: int
    year: int
    category: str
    limit_amount: float
    spent_amount: float
    created_at: datetime


class BudgetUpdate(SQLModel):
    month: int | None = None
    year: int | None = None
    category: str | None = None
    limit_amount: float | None = None
    spent_amount: float | None = None
