from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.database import get_db
from src.auth.models import User, KYCStatus
from src.auth.schemas import UserCreate, UserResponse, Token, VerifyOTPRequest
from src.auth.service import get_password_hash, verify_password, create_access_token
from src.config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import random

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# In-memory store for OTPs
# Structure: email -> {"otp": "123456", "user_data": UserCreate, "expires_at": datetime}
otp_store = {}

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    otp = f"{random.randint(100000, 999999)}"
    
    otp_store[user.email] = {
        "otp": otp,
        "user_data": user,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    
    # Mock Email sending
    print("\n" + "="*40)
    print(f"MOCK EMAIL TO: {user.email}")
    print(f"SUBJECT: Your NeoVault Account Verification OTP")
    print(f"OTP CODE: {otp}")
    print("="*40 + "\n")
    
    return {"message": "OTP sent to email. Please verify to activate account.", "email": user.email}

@router.post("/verify-otp", response_model=UserResponse)
async def verify_otp(data: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    record = otp_store.get(data.email)
    
    if not record:
        raise HTTPException(status_code=400, detail="OTP not found or already verified")
        
    if record["expires_at"] < datetime.now(timezone.utc):
        del otp_store[data.email]
        raise HTTPException(status_code=400, detail="OTP expired. Please register again.")
        
    if record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    # Valid OTP, create user
    user = record["user_data"]
    
    # Check again if user exists to prevent race conditions
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        del otp_store[data.email]
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        phone=user.phone,
        kyc_status=KYCStatus.unverified
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Clean up OTP
    del otp_store[data.email]
    
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
