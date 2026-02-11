import enum
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class KycStatus(str, enum.Enum):
    unverified = "unverified"
    verified = "verified"


# ---------------------------------------------------------------------------
# Database table
# ---------------------------------------------------------------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True, index=True)
    password: str = Field(max_length=255)
    phone: str = Field(max_length=50)
    kyc_status: KycStatus = Field(default=KycStatus.unverified)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    phone: str
    kyc_status: KycStatus
    created_at: datetime


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    kyc_status: KycStatus | None = None
