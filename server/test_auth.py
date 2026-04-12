import asyncio
from datetime import timedelta
from src.auth.router import create_access_token
from src.auth.router import ACCESS_TOKEN_EXPIRE_MINUTES

token = create_access_token(
    data={"sub": "aditya@example.com"},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
)
print(token)
