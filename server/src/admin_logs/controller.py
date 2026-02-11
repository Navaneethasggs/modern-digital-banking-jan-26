from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.admin_logs.models import AdminLogCreate, AdminLogRead, AdminLogUpdate
from src.admin_logs.service import AdminLogService
from src.auth.dependencies import get_current_user
from src.database.core import get_session
from src.users.models import User

router = APIRouter()


@router.post("/", response_model=AdminLogRead, status_code=status.HTTP_201_CREATED)
def create_admin_log(
    data: AdminLogCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AdminLogService.create(session, current_user.id, data)


@router.get("/", response_model=list[AdminLogRead])
def list_admin_logs(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AdminLogService.get_all(session)


@router.get("/{log_id}", response_model=AdminLogRead)
def get_admin_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AdminLogService.get_by_id(session, log_id)


@router.put("/{log_id}", response_model=AdminLogRead)
def update_admin_log(
    log_id: int,
    data: AdminLogUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return AdminLogService.update(session, log_id, data)


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    AdminLogService.delete(session, log_id)
