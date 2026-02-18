from fastapi import Request, HTTPException

from .service import decode_app_jwt


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("sso_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_app_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


def require_agent(slug: str):
    async def dependency(request: Request) -> dict:
        user = await get_current_user(request)
        agents = user.get("agents", [])
        if slug not in agents:
            raise HTTPException(status_code=403, detail=f"Missing agent access: {slug}")
        return user
    return dependency
