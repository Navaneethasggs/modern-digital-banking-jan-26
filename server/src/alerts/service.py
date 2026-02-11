from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.alerts.models import Alert, AlertCreate, AlertUpdate


class AlertService:
    @staticmethod
    def create(session: Session, user_id: int, data: AlertCreate) -> Alert:
        alert = Alert(**data.model_dump(), user_id=user_id)
        session.add(alert)
        session.commit()
        session.refresh(alert)
        return alert

    @staticmethod
    def get_all(session: Session, user_id: int) -> list[Alert]:
        statement = select(Alert).where(Alert.user_id == user_id)
        return list(session.exec(statement).all())

    @staticmethod
    def get_by_id(session: Session, alert_id: int, user_id: int) -> Alert:
        alert = session.get(Alert, alert_id)
        if not alert or alert.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found",
            )
        return alert

    @staticmethod
    def update(
        session: Session, alert_id: int, user_id: int, data: AlertUpdate
    ) -> Alert:
        alert = AlertService.get_by_id(session, alert_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(alert, key, value)
        session.add(alert)
        session.commit()
        session.refresh(alert)
        return alert

    @staticmethod
    def delete(session: Session, alert_id: int, user_id: int) -> None:
        alert = AlertService.get_by_id(session, alert_id, user_id)
        session.delete(alert)
        session.commit()
