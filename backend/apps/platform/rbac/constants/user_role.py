"""
User role constants.
"""

from __future__ import annotations

from django.db import models


class UserRoleAssignmentSource(
    models.TextChoices,
):
    """
    Source of a user-role assignment.
    """

    SYSTEM = (
        "system",
        "System",
    )

    MANUAL = (
        "manual",
        "Manual",
    )

    SSO = (
        "sso",
        "Single Sign-On",
    )

    API = (
        "api",
        "API",
    )


DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE = UserRoleAssignmentSource.SYSTEM


__all__ = [
    "DEFAULT_USER_ROLE_ASSIGNMENT_SOURCE",
    "UserRoleAssignmentSource",
]
