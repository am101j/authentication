from sqlalchemy import Table, Column, Integer, ForeignKey

from .base import Base

role_agent = Table(
    "role_agents",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("agent_id", Integer, ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True),
)
