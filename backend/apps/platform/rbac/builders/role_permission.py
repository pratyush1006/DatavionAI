"""
Role permission builder.
"""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_PERMISSION_SOURCE,
    DEFAULT_ROLE_PERMISSION_TYPE,
)


class RolePermissionBuilder:
    """
    Builder for RolePermission data.
    """

    @classmethod
    def build_create(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build normalized data for creating a role permission.
        """

        return {
            **validated_data,
            "assignment_type": validated_data.get(
                "assignment_type",
                DEFAULT_ROLE_PERMISSION_TYPE,
            ),
            "assignment_source": validated_data.get(
                "assignment_source",
                DEFAULT_ROLE_PERMISSION_SOURCE,
            ),
        }

    @classmethod
    def build_update(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build normalized data for updating a role permission.
        """

        return {
            **validated_data,
        }

    @classmethod
    def build(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build normalized role permission data.
        """

        return cls.build_create(
            validated_data=validated_data,
        )


__all__ = [
    "RolePermissionBuilder",
]
