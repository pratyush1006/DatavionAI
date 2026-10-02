"""
Organization role constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class OrganizationRoleAssignmentSource(
    TextChoices,
):
    """
    Source of an organization role assignment.
    """

    MANUAL = (
        "manual",
        "Manual",
    )

    INVITATION = (
        "invitation",
        "Invitation",
    )

    DEFAULT_ROLE = (
        "default_role",
        "Default Role",
    )

    SYNC = (
        "sync",
        "Synchronization",
    )

    MIGRATION = (
        "migration",
        "Migration",
    )

    SYSTEM = (
        "system",
        "System",
    )


DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE = OrganizationRoleAssignmentSource.MANUAL


__all__ = [
    "DEFAULT_ORGANIZATION_ROLE_ASSIGNMENT_SOURCE",
    "OrganizationRoleAssignmentSource",
]
