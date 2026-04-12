from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BudgetBase(BaseModel):
    month: int
    year: int
    category: str
    limit_amount: float

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    category: Optional[str] = None
    limit_amount: Optional[float] = None
    month: Optional[int] = None
    year: Optional[int] = None

class BudgetResponse(BudgetBase):
    id: int
    spent_amount: float
    is_ai_generated: bool = False
    confidence_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
