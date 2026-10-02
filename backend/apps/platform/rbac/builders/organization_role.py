"""
Organization role builders.
"""

from __future__ import annotations

from typing import Any


class OrganizationRoleBuilder:
    """
    Builder for OrganizationRole.
    """

    @staticmethod
    def build_create(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build validated data for creating an organization role.
        """

        return dict(validated_data)

    @staticmethod
    def build_update(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build validated data for updating an organization role.
        """

        return dict(validated_data)


__all__ = [
    "OrganizationRoleBuilder",
]
