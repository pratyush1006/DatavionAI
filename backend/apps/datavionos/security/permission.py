"""
Permission contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PermissionScope(
    StrEnum,
):
    """
    Permission scope.
    """

    SYSTEM = "system"

    TENANT = "tenant"

    ORGANIZATION = "organization"

    RESOURCE = "resource"


@dataclass(
    frozen=True,
    slots=True,
)
class Permission:
    """
    Immutable authorization permission.
    """

    name: str

    display_name: str

    scope: PermissionScope

    description: str | None = None

    metadata: dict[str, str] | None = None

    @property
    def resource(
        self,
    ) -> str:
        """
        Return the resource namespace.

        Example:
            patients.read -> patients
        """
        return self.name.partition(".")[0]

    @property
    def action(
        self,
    ) -> str:
        """
        Return the permission action.

        Example:
            patients.read -> read
        """
        return self.name.rpartition(".")[2]


__all__ = [
    "Permission",
    "PermissionScope",
]
