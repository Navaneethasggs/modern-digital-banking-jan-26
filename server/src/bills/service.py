from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.bills.models import Bill, BillCreate, BillUpdate


class BillService:
    @staticmethod
    def create(session: Session, user_id: int, data: BillCreate) -> Bill:
        bill = Bill(**data.model_dump(), user_id=user_id)
        session.add(bill)
        session.commit()
        session.refresh(bill)
        return bill

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Bill]:
        statement = select(Bill).where(Bill.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, bill_id: int, user_id: int) -> Bill:
        bill = session.get(Bill, bill_id)
        if not bill or bill.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bill not found",
            )
        return bill

    @staticmethod
    def update(
        session: Session, bill_id: int, user_id: int, data: BillUpdate
    ) -> Bill:
        bill = BillService.get_by_id(session, bill_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(bill, key, value)
        session.add(bill)
        session.commit()
        session.refresh(bill)
        return bill

    @staticmethod
    def delete(session: Session, bill_id: int, user_id: int) -> None:
        bill = BillService.get_by_id(session, bill_id, user_id)
        session.delete(bill)
        session.commit()
