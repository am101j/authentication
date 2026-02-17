from pydantic import BaseModel


class UserMeResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    permissions: list[str]
