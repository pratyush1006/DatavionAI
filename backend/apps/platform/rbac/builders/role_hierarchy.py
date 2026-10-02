"""
Role hierarchy builders.
"""

from __future__ import annotations

from typing import Any


class RoleHierarchyBuilder:
    """
    Builder for RoleHierarchy.
    """

    @staticmethod
    def build_create(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build validated data for creating a role hierarchy.
        """

        return dict(
            validated_data,
        )

    @staticmethod
    def build_update(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build validated data for updating a role hierarchy.
        """

        return dict(
            validated_data,
        )


__all__ = [
    "RoleHierarchyBuilder",
]
