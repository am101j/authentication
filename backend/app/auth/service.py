import json
from datetime import datetime, timezone, timedelta

import jwt
import msal
from itsdangerous import URLSafeTimedSerializer

from ..config import settings

_msal_app: msal.ConfidentialClientApplication | None = None
_serializer: URLSafeTimedSerializer | None = None

SCOPES = ["User.Read"]
REDIRECT_PATH = "/auth/callback"


def get_msal_app() -> msal.ConfidentialClientApplication:
    global _msal_app
    if _msal_app is None:
        _msal_app = msal.ConfidentialClientApplication(
            client_id=settings.ENTRA_CLIENT_ID,
            client_credential=settings.ENTRA_CLIENT_SECRET,
            authority=settings.entra_authority,
        )
    return _msal_app


def get_serializer() -> URLSafeTimedSerializer:
    global _serializer
    if _serializer is None:
        _serializer = URLSafeTimedSerializer(settings.JWT_SECRET)
    return _serializer


def build_auth_url(redirect_uri: str) -> tuple[str, dict]:
    app = get_msal_app()
    flow = app.initiate_auth_code_flow(scopes=SCOPES, redirect_uri=redirect_uri)
    auth_uri = flow["auth_uri"]
    return auth_uri, flow


def complete_auth_flow(flow: dict, query_params: dict) -> dict:
    app = get_msal_app()
    result = app.acquire_token_by_auth_code_flow(flow, query_params)
    if "error" in result:
        raise ValueError(f"Auth error: {result.get('error_description', result['error'])}")
    return result


def serialize_flow(flow: dict) -> str:
    serializer = get_serializer()
    return serializer.dumps(json.dumps(flow))


def deserialize_flow(signed_data: str, max_age: int = 600) -> dict:
    serializer = get_serializer()
    raw = serializer.loads(signed_data, max_age=max_age)
    return json.loads(raw)


def mint_app_jwt(
    user_id: int,
    entra_oid: str,
    email: str,
    full_name: str,
    roles: list[str],
    agents: list[str],
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "entra_oid": entra_oid,
        "email": email,
        "full_name": full_name,
        "roles": roles,
        "agents": agents,
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_app_jwt(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
