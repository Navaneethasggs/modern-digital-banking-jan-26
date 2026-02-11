from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.admin_logs.models import AdminLog, AdminLogCreate, AdminLogUpdate


class AdminLogService:
    @staticmethod
    def create(
        session: Session, admin_id: int, data: AdminLogCreate
    ) -> AdminLog:
        log = AdminLog(**data.model_dump(), admin_id=admin_id)
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    @staticmethod
    def get_all(session: Session) -> list[AdminLog]:
        statement = select(AdminLog)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, log_id: int) -> AdminLog:
        log = session.get(AdminLog, log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin log not found",
            )
        return log

    @staticmethod
    def update(
        session: Session, log_id: int, data: AdminLogUpdate
    ) -> AdminLog:
        log = AdminLogService.get_by_id(session, log_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(log, key, value)
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    @staticmethod
    def delete(session: Session, log_id: int) -> None:
        log = AdminLogService.get_by_id(session, log_id)
        session.delete(log)
        session.commit()
