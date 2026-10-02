"""
User role builder.
"""

from __future__ import annotations

from typing import Any


class UserRoleBuilder:
    """
    Builder for UserRole data.
    """

    @staticmethod
    def build_create(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Prepare data for creating a user role.
        """

        return {
            **validated_data,
        }

    @staticmethod
    def build_update(
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Prepare data for updating a user role.
        """

        return {
            **validated_data,
        }


__all__ = [
    "UserRoleBuilder",
]
