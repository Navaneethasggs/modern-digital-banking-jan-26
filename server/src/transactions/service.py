from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.accounts.models import Account
from src.transactions.models import Transaction, TransactionCreate, TransactionUpdate


class TransactionService:
    @staticmethod
    def _get_user_account_ids(session: Session, user_id: int) -> list[int]:
        """Get all account IDs belonging to a user."""
        statement = select(Account.id).where(Account.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def create(
        session: Session, user_id: int, data: TransactionCreate
    ) -> Transaction:
        # Verify the account belongs to the user
        account = session.get(Account, data.account_id)
        if not account or account.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found",
            )
        txn = Transaction(**data.model_dump())
        session.add(txn)
        session.commit()
        session.refresh(txn)
        return txn

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Transaction]:
        account_ids = TransactionService._get_user_account_ids(session, user_id)
        if not account_ids:
            return []
        statement = select(Transaction).where(
            Transaction.account_id.in_(account_ids)  # type: ignore[attr-defined]
        )
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(
        session: Session, txn_id: int, user_id: int
    ) -> Transaction:
        txn = session.get(Transaction, txn_id)
        if not txn:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        account_ids = TransactionService._get_user_account_ids(session, user_id)
        if txn.account_id not in account_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        return txn

    @staticmethod
    def update(
        session: Session, txn_id: int, user_id: int, data: TransactionUpdate
    ) -> Transaction:
        txn = TransactionService.get_by_id(session, txn_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(txn, key, value)
        session.add(txn)
        session.commit()
        session.refresh(txn)
        return txn

    @staticmethod
    def delete(session: Session, txn_id: int, user_id: int) -> None:
        txn = TransactionService.get_by_id(session, txn_id, user_id)
        session.delete(txn)
        session.commit()
