from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.alerts.models import AlertCreate, AlertRead, AlertUpdate
from src.alerts.service import AlertService
from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(
    data: AlertCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AlertService.create(session, current_user.id, data)


@router.get("/", response_model=list[AlertRead])
def list_alerts(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AlertService.get_all(session, current_user.id)


@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AlertService.get_by_id(session, alert_id, current_user.id)


@router.put("/{alert_id}", response_model=AlertRead)
def update_alert(
    alert_id: int,
    data: AlertUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AlertService.update(session, alert_id, current_user.id, data)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    AlertService.delete(session, alert_id, current_user.id)
