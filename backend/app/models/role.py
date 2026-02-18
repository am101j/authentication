from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    agents = relationship(
        "Agent", secondary="role_agents", back_populates="roles", lazy="selectin"
    )
    users = relationship("User", secondary="user_roles", back_populates="roles", lazy="noload")
