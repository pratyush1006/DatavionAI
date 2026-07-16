"""
Role permission constants.
"""

from __future__ import annotations

from django.db import models


class RolePermissionType(
    models.TextChoices,
):
    """
    Role permission assignment type.
    """

    DIRECT = (
        "direct",
        "Direct",
    )

    INHERITED = (
        "inherited",
        "Inherited",
    )


DEFAULT_ROLE_PERMISSION_TYPE = RolePermissionType.DIRECT


class RolePermissionSource(
    models.TextChoices,
):
    """
    Source of the permission assignment.
    """

    SYSTEM = (
        "system",
        "System",
    )

    ORGANIZATION = (
        "organization",
        "Organization",
    )

    USER = (
        "user",
        "User",
    )


DEFAULT_ROLE_PERMISSION_SOURCE = RolePermissionSource.SYSTEM


__all__ = [
    "DEFAULT_ROLE_PERMISSION_SOURCE",
    "DEFAULT_ROLE_PERMISSION_TYPE",
    "RolePermissionSource",
    "RolePermissionType",
]
