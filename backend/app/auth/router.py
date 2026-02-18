from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db
from ..models import User
from . import service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login(request: Request):
    redirect_uri = str(request.url_for("auth_callback"))
    auth_uri, flow = service.build_auth_url(redirect_uri)

    signed_flow = service.serialize_flow(flow)

    response = RedirectResponse(url=auth_uri, status_code=302)
    response.set_cookie(
        key="auth_flow",
        value=signed_flow,
        httponly=True,
        path="/auth/callback",
        max_age=600,
        samesite="lax",
    )
    return response


@router.get("/callback", name="auth_callback")
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    signed_flow = request.cookies.get("auth_flow")
    if not signed_flow:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=missing_flow")

    try:
        flow = service.deserialize_flow(signed_flow)
    except Exception:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=invalid_flow")

    try:
        result = service.complete_auth_flow(flow, dict(request.query_params))
    except ValueError:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=auth_failed")

    claims = result.get("id_token_claims", {})
    oid = claims.get("oid", "")
    email = claims.get("preferred_username", claims.get("email", ""))
    full_name = claims.get("name", "")

    # Upsert user
    stmt = select(User).where(User.entra_oid == oid)
    db_result = await db.execute(stmt)
    user = db_result.scalar_one_or_none()

    if user is None:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=unknown_user")

    # Resolve roles -> agents from ORM relationships
    role_names = [r.name for r in user.roles]
    agent_slugs = list({a.slug for r in user.roles for a in r.agents})

    token = service.mint_app_jwt(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=role_names,
        agents=agent_slugs,
    )

    response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)
    # Delete the auth_flow cookie
    response.delete_cookie(key="auth_flow", path="/auth/callback")
    # Set the session token
    response.set_cookie(
        key="sso_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )
    return response


@router.get("/dev-login")
async def dev_login(user_id: int, db: AsyncSession = Depends(get_db)):
    """Dev-only: bypass Entra and log in as a seeded test user."""
    stmt = select(User).where(User.id == user_id)
    db_result = await db.execute(stmt)
    user = db_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    role_names = [r.name for r in user.roles]
    agent_slugs = list({a.slug for r in user.roles for a in r.agents})

    token = service.mint_app_jwt(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=role_names,
        agents=agent_slugs,
    )

    response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)
    response.set_cookie(
        key="sso_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.JWT_EXPIRATION_MINUTES * 60,
        path="/",
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)
    response.delete_cookie(key="sso_token", path="/")
    return response
