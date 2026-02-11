from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.budgets.models import BudgetCreate, BudgetRead, BudgetUpdate
from src.budgets.service import BudgetService
from src.database.core import get_session
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(
    data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BudgetService.create(session, current_user.id, data)


@router.get("/", response_model=list[BudgetRead])
def list_budgets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BudgetService.get_all(session, current_user.id)


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BudgetService.get_by_id(session, budget_id, current_user.id)


@router.put("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: int,
    data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return BudgetService.update(session, budget_id, current_user.id, data)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    BudgetService.delete(session, budget_id, current_user.id)
