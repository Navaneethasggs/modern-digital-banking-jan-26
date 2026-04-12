from pydantic import BaseModel
from typing import List, Optional

class GenerateBudgetRequest(BaseModel):
    """Request body for POST /ai/generate-budget"""
    save: bool = False  # If True, persist recommendations as Budget records

class BudgetRecommendation(BaseModel):
    """Single category budget recommendation"""
    category: str
    recommended_limit: float
    confidence: float                # 0.0 – 1.0
    reasoning: str                   # Human-readable explanation for UI tooltip
    current_budget: Optional[float]  # Existing budget limit (None if no budget set)
    predicted_spend: float           # Forecasted next-month spend
    trend: str                       # "increasing", "decreasing", or "stable"
    avg_monthly_spend: float         # Historical average
    is_essential: bool               # Essential vs discretionary classification

class PredictionAlert(BaseModel):
    """Alert generated when predicted spend exceeds budget"""
    category: str
    predicted_spend: float
    budget_limit: float
    message: str

class AIBudgetResponse(BaseModel):
    """Full response from budget generation endpoint"""
    recommendations: List[BudgetRecommendation]
    total_recommended: float
    estimated_income: float
    alerts: List[PredictionAlert]
