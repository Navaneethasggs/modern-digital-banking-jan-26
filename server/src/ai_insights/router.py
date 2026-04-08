from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import google.generativeai as genai
from pydantic import BaseModel

from src.database import get_db
from src.auth.router import get_current_user
from src.auth.models import User
from src.transactions.models import Transaction, TransactionType
from src.accounts.models import Account
from src.config import settings
import json

router = APIRouter()

class SummaryResponse(BaseModel):
    summary: str

@router.get("/summary", response_model=SummaryResponse)
async def get_weekly_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key is missing from configuration.")

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Gemini: {str(e)}")

    # Fetch last 30 days of transactions for better context, but summarize recent
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    result = await db.execute(
        select(Transaction)
        .join(Account)
        .filter(Account.user_id == current_user.id, Transaction.txn_date >= thirty_days_ago)
        .order_by(Transaction.txn_date.desc())
    )
    transactions = result.scalars().all()
    
    if not transactions:
        return SummaryResponse(summary="It looks like you don't have any recent transactions to analyze. Start adding some expenses or income to get your personalized financial summary!")

    # Prepare data for LLM
    total_debit = sum(t.amount for t in transactions if t.txn_type == TransactionType.debit)
    total_credit = sum(t.amount for t in transactions if t.txn_type == TransactionType.credit)
    
    categories = {}
    for t in transactions:
        if t.txn_type == TransactionType.debit:
            categories[t.category] = categories.get(t.category, 0) + t.amount

    recent_txns = transactions[:10]  # Just give the 10 most recent for context
    txn_context = []
    for t in recent_txns:
        txn_context.append(f"- {t.txn_date.strftime('%Y-%m-%d')}: {t.description} (₹{t.amount}) [{t.category}]")

    prompt = f"""
    You are a friendly, expert financial AI assistant inside the 'NeoVault' banking app.
    Please provide a concise, engaging, and personalized financial summary based on the following user data from the last 30 days.

    Data:
    - Total Income (Credit): ₹{total_credit}
    - Total Expenses (Debit): ₹{total_debit}
    - Top Spending Categories: {json.dumps(categories, indent=2)}
    
    10 Most Recent Transactions:
    {chr(10).join(txn_context)}
    
    Instructions:
    1. Start with a warm greeting and a 2-3 sentence high-level summary of their financial health based on income vs expenses.
    2. Add exactly 3 bullet points with specific, actionable insights or observations based on their categories or recent transactions.
    3. Use Markdown formatting. Make it look beautiful and easy to read.
    4. Keep the tone encouraging, professional, and helpful.
    """

    try:
        response = model.generate_content(prompt)
        return SummaryResponse(summary=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
