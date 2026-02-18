from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str
    email: str
    full_name: str
    roles: list[str]
    agents: list[str]
