from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """Request body for user registration."""

    name: str
    email: EmailStr
    password: str
    phone: str


class UserLogin(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response body after successful login."""

    access_token: str
    token_type: str = "bearer"
