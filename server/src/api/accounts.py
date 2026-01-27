from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/")
def get_accounts():
    return []
