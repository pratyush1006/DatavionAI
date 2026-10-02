"""
Role permission builder.

Normalizes RolePermission assignment data
for DatavionOS RBAC workflows.
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

    @staticmethod
    def _normalize_choice(
        value,
    ):
        """
        Normalize TextChoices values.

        Supports:
        - Enum instance
        - Raw string
        """

        if hasattr(
            value,
            "value",
        ):
            return value.value

        return value

    @classmethod
    def build_create(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build normalized data for creation.
        """

        data = {
            **validated_data,
        }

        data["assignment_type"] = cls._normalize_choice(
            data.get(
                "assignment_type",
                DEFAULT_ROLE_PERMISSION_TYPE,
            )
        )

        data["assignment_source"] = cls._normalize_choice(
            data.get(
                "assignment_source",
                DEFAULT_ROLE_PERMISSION_SOURCE,
            )
        )

        return data

    @classmethod
    def build_update(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build normalized data for update.
        """

        data = {
            **validated_data,
        }

        if "assignment_type" in data:
            data["assignment_type"] = cls._normalize_choice(
                data["assignment_type"],
            )

        if "assignment_source" in data:
            data["assignment_source"] = cls._normalize_choice(
                data["assignment_source"],
            )

        return data

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
