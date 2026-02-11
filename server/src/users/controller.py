from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.users.models import User, UserRead, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Update the current authenticated user's profile."""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete the current authenticated user's account."""
    session.delete(current_user)
    session.commit()
