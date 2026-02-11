from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.accounts.models import AccountCreate, AccountRead, AccountUpdate
from src.accounts.service import AccountService
from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(
    data: AccountCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AccountService.create(session, current_user.id, data)


@router.get("/", response_model=list[AccountRead])
def list_accounts(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AccountService.get_all(session, current_user.id)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AccountService.get_by_id(session, account_id, current_user.id)


@router.put("/{account_id}", response_model=AccountRead)
def update_account(
    account_id: int,
    data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AccountService.update(session, account_id, current_user.id, data)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    AccountService.delete(session, account_id, current_user.id)
