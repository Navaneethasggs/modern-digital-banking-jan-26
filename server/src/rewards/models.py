from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class Reward(SQLModel, table=True):
    __tablename__ = "rewards"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    program_name: str = Field(max_length=255)
    points_balance: int = Field(default=0)
    last_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class RewardCreate(SQLModel):
    program_name: str
    points_balance: int = 0


class RewardRead(SQLModel):
    id: int
    user_id: int
    program_name: str
    points_balance: int
    last_updated: datetime


class RewardUpdate(SQLModel):
    program_name: str | None = None
    points_balance: int | None = None
