"""Idempotent seed script for agents, roles, and role-agent mappings.

Usage: python -m app.seed
"""

import asyncio

from sqlalchemy import select

from .database import async_session
from .models import Base, Agent, Role, User, role_agent, user_role


AGENTS = [
    ("Design Agent", "design-agent"),
    ("Developer Agent", "developer-agent"),
    ("Testing Agent", "testing-agent"),
]

ROLES = {
    "Deposit Tester": ["testing-agent"],
    "Deposit Design": ["design-agent"],
    "Lending Tester": ["testing-agent"],
    "Developer": ["developer-agent"],
}


async def create_tables():
    """Create all tables from models (for dev use without Alembic)."""
    from .database import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed():
    await create_tables()
    async with async_session() as session:
        async with session.begin():
            # Upsert agents
            agent_map: dict[str, Agent] = {}
            for name, slug in AGENTS:
                result = await session.execute(select(Agent).where(Agent.slug == slug))
                ag = result.scalar_one_or_none()
                if not ag:
                    ag = Agent(name=name, slug=slug)
                    session.add(ag)
                    await session.flush()
                agent_map[slug] = ag

            # Upsert roles and assign agents
            for role_name, agent_slugs in ROLES.items():
                result = await session.execute(select(Role).where(Role.name == role_name))
                role = result.scalar_one_or_none()
                if not role:
                    role = Role(name=role_name)
                    session.add(role)
                    await session.flush()

                # Check existing associations
                existing = await session.execute(
                    select(role_agent.c.agent_id).where(
                        role_agent.c.role_id == role.id
                    )
                )
                existing_ids = {row[0] for row in existing}

                for slug in agent_slugs:
                    ag = agent_map[slug]
                    if ag.id not in existing_ids:
                        await session.execute(
                            role_agent.insert().values(
                                role_id=role.id, agent_id=ag.id
                            )
                        )

            # Upsert test users and assign roles
            test_users = [
                ("Alice", "dev-alice", "alice@localhost", ["Deposit Tester"]),
                ("Bob", "dev-bob", "bob@localhost", ["Developer"]),
                ("Carol", "dev-carol", "carol@localhost", ["Deposit Design", "Developer"]),
            ]

            # Build role lookup
            role_result = await session.execute(select(Role))
            role_map = {r.name: r for r in role_result.scalars()}

            for full_name, entra_oid, email, role_names in test_users:
                result = await session.execute(
                    select(User).where(User.entra_oid == entra_oid)
                )
                user = result.scalar_one_or_none()
                if not user:
                    user = User(entra_oid=entra_oid, email=email, full_name=full_name)
                    session.add(user)
                    await session.flush()

                # Check existing role assignments
                existing = await session.execute(
                    select(user_role.c.role_id).where(
                        user_role.c.user_id == user.id
                    )
                )
                existing_role_ids = {row[0] for row in existing}

                for rn in role_names:
                    r = role_map[rn]
                    if r.id not in existing_role_ids:
                        await session.execute(
                            user_role.insert().values(
                                user_id=user.id, role_id=r.id
                            )
                        )

    print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())


def main():
    asyncio.run(seed())
