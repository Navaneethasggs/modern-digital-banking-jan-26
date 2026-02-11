from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.transactions.models import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from src.transactions.service import TransactionService
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return TransactionService.create(session, current_user.id, data)


@router.get("/", response_model=list[TransactionRead])
def list_transactions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return TransactionService.get_all(session, current_user.id)


@router.get("/{txn_id}", response_model=TransactionRead)
def get_transaction(
    txn_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return TransactionService.get_by_id(session, txn_id, current_user.id)


@router.put("/{txn_id}", response_model=TransactionRead)
def update_transaction(
    txn_id: int,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return TransactionService.update(session, txn_id, current_user.id, data)


@router.delete("/{txn_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    txn_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    TransactionService.delete(session, txn_id, current_user.id)
