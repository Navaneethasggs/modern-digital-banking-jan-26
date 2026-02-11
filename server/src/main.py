from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.database.core import init_db

# Import all models so SQLModel registers them before create_all
import src.users.models  # noqa: F401
import src.accounts.models  # noqa: F401
import src.transactions.models  # noqa: F401
import src.bills.models  # noqa: F401
import src.rewards.models  # noqa: F401
import src.budgets.models  # noqa: F401
import src.alerts.models  # noqa: F401
import src.admin_logs.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: runs init_db on startup to auto-create tables."""
    init_db()
    yield


app = FastAPI(
    title="NeoVault API",
    description="Modern Digital Banking API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
