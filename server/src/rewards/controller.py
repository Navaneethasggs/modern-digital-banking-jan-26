from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.rewards.models import RewardCreate, RewardRead, RewardUpdate
from src.rewards.service import RewardService
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=RewardRead, status_code=status.HTTP_201_CREATED)
def create_reward(
    data: RewardCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return RewardService.create(session, current_user.id, data)


@router.get("/", response_model=list[RewardRead])
def list_rewards(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return RewardService.get_all(session, current_user.id)


@router.get("/{reward_id}", response_model=RewardRead)
def get_reward(
    reward_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return RewardService.get_by_id(session, reward_id, current_user.id)


@router.put("/{reward_id}", response_model=RewardRead)
def update_reward(
    reward_id: int,
    data: RewardUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return RewardService.update(session, reward_id, current_user.id, data)


@router.delete("/{reward_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reward(
    reward_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    RewardService.delete(session, reward_id, current_user.id)
