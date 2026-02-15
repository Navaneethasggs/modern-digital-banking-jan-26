
import asyncio
import sys
import os

# Add src to path to allow imports
sys.path.append(os.getcwd())

from src.database import SessionLocal
from src.auth.models import User, KYCStatus
from src.auth.service import get_password_hash
from sqlalchemy.future import select

async def create_users():
    async with SessionLocal() as session:
        # Create Admin User
        result = await session.execute(select(User).where(User.email == "admin@neovault.com"))
        user = result.scalars().first()
        if not user:
            print("Creating admin user...")
            hashed_pw = get_password_hash("admin123")
            new_user = User(
                name="Admin User",
                email="admin@neovault.com",
                hashed_password=hashed_pw,
                phone="1234567890",
                kyc_status=KYCStatus.verified
            )
            session.add(new_user)
            await session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        # Create Regular User
        result = await session.execute(select(User).where(User.email == "aditya@example.com"))
        user = result.scalars().first()
        if not user:
            print("Creating regular user...")
            hashed_pw = get_password_hash("password123")
            new_user = User(
                name="Aditya",
                email="aditya@example.com",
                hashed_password=hashed_pw,
                phone="0987654321",
                kyc_status=KYCStatus.verified
            )
            session.add(new_user)
            await session.commit()
            print("Regular user created.")
        else:
            print("Regular user already exists.")

if __name__ == "__main__":
    asyncio.run(create_users())
