from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.accounts.router import router as accounts_router
from src.transactions.router import router as transactions_router
from src.budgets.router import router as budgets_router
from src.bills.router import router as bills_router
from src.analytics.router import router as analytics_router
from src.ai_insights.router import router as ai_insights_router
from src.ai_budget.router import router as ai_budget_router

app = FastAPI(title="NeoVault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
app.include_router(budgets_router, prefix="/budgets", tags=["Budgets"])
app.include_router(bills_router, prefix="/bills", tags=["Bills & Rewards"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics & Alerts"])
app.include_router(ai_insights_router, prefix="/ai-insights", tags=["AI Insights"])
app.include_router(ai_budget_router, prefix="/ai", tags=["AI Budget"])
