from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.accounts.models import Account, AccountCreate, AccountUpdate


class AccountService:
    @staticmethod
    def create(session: Session, user_id: int, data: AccountCreate) -> Account:
        account = Account(**data.model_dump(), user_id=user_id)
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Account]:
        statement = select(Account).where(Account.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, account_id: int, user_id: int) -> Account:
        account = session.get(Account, account_id)
        if not account or account.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found",
            )
        return account

    @staticmethod
    def update(
        session: Session, account_id: int, user_id: int, data: AccountUpdate
    ) -> Account:
        account = AccountService.get_by_id(session, account_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(account, key, value)
        session.add(account)
        session.commit()
        session.refresh(account)
        return account

    @staticmethod
    def delete(session: Session, account_id: int, user_id: int) -> None:
        account = AccountService.get_by_id(session, account_id, user_id)
        session.delete(account)
        session.commit()
