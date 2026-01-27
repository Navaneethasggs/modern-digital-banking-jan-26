from fastapi import FastAPI

from src.api.users import router as users_router
from src.api.accounts import router as accounts_router
from src.api.transactions import router as transactions_router
from src.api.bills import router as bills_router
from src.api.budgets import router as budgets_router
from src.api.rewards import router as rewards_router
from src.api.alerts import router as alerts_router
from src.api.auth import router as auth_router

app = FastAPI(title="NeoVault API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(bills_router)
app.include_router(budgets_router)
app.include_router(rewards_router)
app.include_router(alerts_router)

@app.get("/health")
def health():
    return {"status": "ok"}
