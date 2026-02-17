from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    email: str
    full_name: str
    role: str
    permissions: list[str]
