from fastapi import APIRouter

from src.accounts.controller import router as accounts_router
from src.admin_logs.controller import router as admin_logs_router
from src.alerts.controller import router as alerts_router
from src.auth.controller import router as auth_router
from src.bills.controller import router as bills_router
from src.budgets.controller import router as budgets_router
from src.rewards.controller import router as rewards_router
from src.transactions.controller import router as transactions_router
from src.users.controller import router as users_router

api_router = APIRouter()


@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(
    transactions_router, prefix="/transactions", tags=["Transactions"]
)
api_router.include_router(bills_router, prefix="/bills", tags=["Bills"])
api_router.include_router(rewards_router, prefix="/rewards", tags=["Rewards"])
api_router.include_router(budgets_router, prefix="/budgets", tags=["Budgets"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(
    admin_logs_router, prefix="/admin-logs", tags=["Admin Logs"]
)
