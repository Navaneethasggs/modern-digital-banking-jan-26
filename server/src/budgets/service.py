from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.budgets.models import Budget, BudgetCreate, BudgetUpdate


class BudgetService:
    @staticmethod
    def create(session: Session, user_id: int, data: BudgetCreate) -> Budget:
        budget = Budget(**data.model_dump(), user_id=user_id)
        session.add(budget)
        session.commit()
        session.refresh(budget)
        return budget

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Budget]:
        statement = select(Budget).where(Budget.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, budget_id: int, user_id: int) -> Budget:
        budget = session.get(Budget, budget_id)
        if not budget or budget.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found",
            )
        return budget

    @staticmethod
    def update(
        session: Session, budget_id: int, user_id: int, data: BudgetUpdate
    ) -> Budget:
        budget = BudgetService.get_by_id(session, budget_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(budget, key, value)
        session.add(budget)
        session.commit()
        session.refresh(budget)
        return budget

    @staticmethod
    def delete(session: Session, budget_id: int, user_id: int) -> None:
        budget = BudgetService.get_by_id(session, budget_id, user_id)
        session.delete(budget)
        session.commit()
