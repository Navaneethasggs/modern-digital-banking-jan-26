import asyncio
from src.database import SessionLocal
from src.ai_budget.service import generate_budget_recommendations, save_ai_budgets

async def test():
    async with SessionLocal() as db:
        # Assuming user_id=3 is the test user from earlier sqlite dump
        result = await generate_budget_recommendations(db, 3)
        print("Recommendations generated:", len(result["recommendations"]))
        
        # Test save
        saved = await save_ai_budgets(db, 3, result["recommendations"], 4, 2026)
        print("Saved budgets:", len(saved))

asyncio.run(test())
