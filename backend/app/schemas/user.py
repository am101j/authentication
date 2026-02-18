from pydantic import BaseModel


class UserMeResponse(BaseModel):
    id: int
    entra_oid: str
    email: str
    full_name: str
    roles: list[str]
    agents: list[str]
