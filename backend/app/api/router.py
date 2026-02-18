from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_user
from ..schemas.user import UserMeResponse

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/user/me", response_model=UserMeResponse)
async def get_me(user: dict = Depends(get_current_user)):
    return UserMeResponse(
        id=int(user["sub"]),
        entra_oid=user["entra_oid"],
        email=user["email"],
        full_name=user["full_name"],
        roles=user["roles"],
        agents=user["agents"],
    )
