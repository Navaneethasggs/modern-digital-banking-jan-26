
import asyncio
import sys
import os
import random
from datetime import datetime, timedelta, date

# Add src to path to allow imports
sys.path.append(os.getcwd())

from src.database import SessionLocal
from src.auth.models import User
from src.accounts.models import Account, AccountType
from src.transactions.models import Transaction, TransactionType
from src.budgets.models import Budget
from src.bills.models import Bill, BillStatus, Reward
from sqlalchemy.future import select

async def seed_data():
    # Use expire_on_commit=False to prevent "MissingGreenlet" on attribute access after commit
    async with SessionLocal() as session:
        # Get the regular user
        result = await session.execute(select(User).where(User.email == "test@test.com"))
        user = result.scalars().first()
        
        if not user:
            print("User 'test@test.com' not found. Please run create_admin.py first.")
            return

        print(f"Seeding data for user: {user.name} ({user.id})")

        # 1. Seed Accounts
        accounts_data = [
            {"bank_name": "HDFC Bank", "account_type": AccountType.checking, "masked_account": "**** 1234", "balance": 54320.10},
            {"bank_name": "SBI Savings", "account_type": AccountType.savings, "masked_account": "**** 5678", "balance": 125000.50},
            {"bank_name": "ICICI Platinum", "account_type": AccountType.credit_card, "masked_account": "**** 9012", "balance": -4500.00},
            {"bank_name": "Zerodha", "account_type": AccountType.investment, "masked_account": "**** 3456", "balance": 89000.00},
        ]

        created_accounts = []
        for acc in accounts_data:
            # Check if account exists
            result = await session.execute(select(Account).where(Account.user_id == user.id, Account.masked_account == acc["masked_account"]))
            existing = result.scalars().first()
            if not existing:
                new_acc = Account(
                    user_id=user.id,
                    bank_name=acc["bank_name"],
                    account_type=acc["account_type"],
                    masked_account=acc["masked_account"],
                    balance=acc["balance"],
                    currency="INR"
                )
                session.add(new_acc)
                created_accounts.append(new_acc)
            else:
                created_accounts.append(existing)
        
        # Flush to get IDs for new accounts without expiring them
        await session.flush()
        print(f"Accounts matched/created: {len(created_accounts)}")

        # 2. Seed Transactions
        categories = ["Food & Dining", "Transportation", "Shopping", "Entertainment", "Bills & Utilities", "Health", "Salary", "Transfer"]
        merchants = ["Swiggy", "Zomato", "Amazon India", "Flipkart", "Reliance Smart", "Jio", "Indian Oil", "Croma"]
        
        transactions_to_add = []
        for acc in created_accounts:
            # Generate 10 random transactions per account
            for _ in range(10):
                is_credit = random.random() > 0.7  # 30% chance of credit/deposit
                amount = round(random.uniform(10.0, 500.0), 2)
                type_ = TransactionType.credit if is_credit else TransactionType.debit
                cat = "Salary" if is_credit else random.choice(categories)
                desc = "Direct Deposit" if is_credit else f"Payment to {random.choice(merchants)}"
                
                txn = Transaction(
                    account_id=acc.id,
                    description=desc,
                    category=cat,
                    amount=amount,
                    currency="INR",
                    txn_type=type_,
                    merchant=random.choice(merchants) if type_ == TransactionType.debit else "Employer",
                    txn_date=datetime.now() - timedelta(days=random.randint(0, 60)),
                    posted_date=datetime.now() - timedelta(days=random.randint(0, 60))
                )
                transactions_to_add.append(txn)
        
        session.add_all(transactions_to_add)
        print(f"Seeding {len(transactions_to_add)} transactions...")

        # 3. Seed Budgets
        budgets_data = [
            {"category": "Food & Dining", "limit": 15000.00, "spent": 12450.00},
            {"category": "Transportation", "limit": 5000.00, "spent": 2120.00},
            {"category": "Entertainment", "limit": 4000.00, "spent": 3180.00},
            {"category": "Shopping", "limit": 10000.00, "spent": 8350.00},
        ]
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        for bg in budgets_data:
             # Check if budget exists
            result = await session.execute(select(Budget).where(Budget.user_id == user.id, Budget.category == bg["category"], Budget.month == current_month))
            existing = result.scalars().first()
            if not existing:
                new_budget = Budget(
                    user_id=user.id,
                    month=current_month,
                    year=current_year,
                    category=bg["category"],
                    limit_amount=bg["limit"],
                    spent_amount=bg["spent"]
                )
                session.add(new_budget)

        print("Seeding budgets...")

        # 4. Seed Bills
        bills_data = [
            {"biller": "BSES Rajdhani", "amount": 2120.50, "date": date.today() + timedelta(days=5), "status": BillStatus.upcoming},
            {"biller": "Jio Fiber", "amount": 999.00, "date": date.today() + timedelta(days=10), "status": BillStatus.upcoming},
            {"biller": "House Rent", "amount": 25000.00, "date": date.today() - timedelta(days=2), "status": BillStatus.paid},
            {"biller": "HDFC Credit Card", "amount": 5200.00, "date": date.today() - timedelta(days=5), "status": BillStatus.overdue},
        ]

        for bill in bills_data:
            # Check for duplicates to allow re-running
            result = await session.execute(select(Bill).where(Bill.user_id == user.id, Bill.biller_name == bill["biller"], Bill.due_date == bill["date"]))
            if not result.scalars().first():
                new_bill = Bill(
                    user_id=user.id,
                    biller_name=bill["biller"],
                    due_date=bill["date"],
                    amount_due=bill["amount"],
                    status=bill["status"],
                    auto_pay=False
                )
                session.add(new_bill)
            
        print("Seeding bills...")

        # 5. Seed Rewards
        reward_check = await session.execute(select(Reward).where(Reward.user_id == user.id))
        if not reward_check.scalars().first():
             new_reward = Reward(
                 user_id=user.id,
                 program_name="NeoVault Gold Rewards",
                 points_balance=12500
             )
             session.add(new_reward)
             print("Seeding rewards...")

        await session.commit()
        print("Data seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
