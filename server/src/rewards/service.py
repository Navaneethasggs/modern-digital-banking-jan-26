from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.rewards.models import Reward, RewardCreate, RewardUpdate


class RewardService:
    @staticmethod
    def create(session: Session, user_id: int, data: RewardCreate) -> Reward:
        reward = Reward(**data.model_dump(), user_id=user_id)
        session.add(reward)
        session.commit()
        session.refresh(reward)
        return reward

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Reward]:
        statement = select(Reward).where(Reward.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, reward_id: int, user_id: int) -> Reward:
        reward = session.get(Reward, reward_id)
        if not reward or reward.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reward not found",
            )
        return reward

    @staticmethod
    def update(
        session: Session, reward_id: int, user_id: int, data: RewardUpdate
    ) -> Reward:
        reward = RewardService.get_by_id(session, reward_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(reward, key, value)
        reward.last_updated = datetime.now(timezone.utc)
        session.add(reward)
        session.commit()
        session.refresh(reward)
        return reward

    @staticmethod
    def delete(session: Session, reward_id: int, user_id: int) -> None:
        reward = RewardService.get_by_id(session, reward_id, user_id)
        session.delete(reward)
        session.commit()
