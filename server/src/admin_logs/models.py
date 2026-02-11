from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class AdminLog(SQLModel, table=True):
    __tablename__ = "adminlogs"

    id: int | None = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="users.id", index=True)
    action: str
    target_type: str = Field(max_length=255)
    target_id: int
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class AdminLogCreate(SQLModel):
    action: str
    target_type: str
    target_id: int


class AdminLogRead(SQLModel):
    id: int
    admin_id: int
    action: str
    target_type: str
    target_id: int
    timestamp: datetime


class AdminLogUpdate(SQLModel):
    action: str | None = None
    target_type: str | None = None
    target_id: int | None = None
