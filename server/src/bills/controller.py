from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.bills.models import BillCreate, BillRead, BillUpdate
from src.bills.service import BillService
from src.database.core import get_session
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=BillRead, status_code=status.HTTP_201_CREATED)
def create_bill(
    data: BillCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BillService.create(session, current_user.id, data)


@router.get("/", response_model=list[BillRead])
def list_bills(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BillService.get_all(session, current_user.id)


@router.get("/{bill_id}", response_model=BillRead)
def get_bill(
    bill_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BillService.get_by_id(session, bill_id, current_user.id)


@router.put("/{bill_id}", response_model=BillRead)
def update_bill(
    bill_id: int,
    data: BillUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BillService.update(session, bill_id, current_user.id, data)


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(
    bill_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    BillService.delete(session, bill_id, current_user.id)
