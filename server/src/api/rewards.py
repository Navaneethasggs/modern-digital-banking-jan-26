from fastapi import APIRouter

router = APIRouter(prefix="/rewards", tags=["Rewards"])

@router.get("/")
def get_rewards():
    return []
