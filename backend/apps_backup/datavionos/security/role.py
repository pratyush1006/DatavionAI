"""
Role contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RoleScope(
    StrEnum,
):
    """
    Role assignment scope.
    """

    SYSTEM = "system"

    TENANT = "tenant"

    ORGANIZATION = "organization"


@dataclass(
    frozen=True,
    slots=True,
)
class Role:
    """
    Immutable authorization role.
    """

    id: str

    name: str

    display_name: str

    scope: RoleScope

    description: str | None = None

    permissions: frozenset[str] = frozenset()

    metadata: dict[str, str] | None = None

    def has_permission(
        self,
        permission: str,
    ) -> bool:
        """
        Determine whether this role
        contains a permission.
        """
        return permission in self.permissions


__all__ = [
    "Role",
    "RoleScope",
]
