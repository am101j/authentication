"""Idempotent seed script for roles and permissions.

Usage: python -m app.seed
"""

import asyncio

from sqlalchemy import select

from .database import async_session
from .models import Role, Permission, role_permission


PERMISSIONS = [
    ("dashboard.view", "View the dashboard"),
    ("dashboard.edit", "Edit dashboard content"),
    ("settings.view", "View settings"),
    ("settings.edit", "Edit settings"),
    ("users.view", "View user list"),
    ("users.manage", "Manage users"),
]

ROLES = {
    "Admin": [
        "dashboard.view", "dashboard.edit",
        "settings.view", "settings.edit",
        "users.view", "users.manage",
    ],
    "User": ["dashboard.view", "dashboard.edit", "settings.view"],
    "Guest": ["dashboard.view"],
}


async def seed():
    async with async_session() as session:
        async with session.begin():
            # Upsert permissions
            perm_map: dict[str, Permission] = {}
            for slug, description in PERMISSIONS:
                result = await session.execute(select(Permission).where(Permission.slug == slug))
                perm = result.scalar_one_or_none()
                if not perm:
                    perm = Permission(slug=slug, description=description)
                    session.add(perm)
                    await session.flush()
                perm_map[slug] = perm

            # Upsert roles and assign permissions
            for role_name, perm_slugs in ROLES.items():
                result = await session.execute(select(Role).where(Role.name == role_name))
                role = result.scalar_one_or_none()
                if not role:
                    role = Role(name=role_name)
                    session.add(role)
                    await session.flush()

                # Check existing associations
                existing = await session.execute(
                    select(role_permission.c.permission_id).where(
                        role_permission.c.role_id == role.id
                    )
                )
                existing_ids = {row[0] for row in existing}

                for slug in perm_slugs:
                    perm = perm_map[slug]
                    if perm.id not in existing_ids:
                        await session.execute(
                            role_permission.insert().values(
                                role_id=role.id, permission_id=perm.id
                            )
                        )

    print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())


def main():
    asyncio.run(seed())
