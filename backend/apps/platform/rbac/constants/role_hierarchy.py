"""
Role hierarchy constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class RoleHierarchyType(
    TextChoices,
):
    """
    Supported role hierarchy types.
    """

    DIRECT = (
        "direct",
        "Direct",
    )

    INHERITED = (
        "inherited",
        "Inherited",
    )


class RoleHierarchyAssignmentSource(
    TextChoices,
):
    """
    Source of the role hierarchy assignment.
    """

    SYSTEM = (
        "system",
        "System",
    )

    MANUAL = (
        "manual",
        "Manual",
    )

    IMPORT = (
        "import",
        "Import",
    )

    API = (
        "api",
        "API",
    )


DEFAULT_ROLE_HIERARCHY_TYPE = RoleHierarchyType.DIRECT

DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE = RoleHierarchyAssignmentSource.SYSTEM

MAX_ROLE_HIERARCHY_DEPTH = 10


__all__ = [
    "DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE",
    "DEFAULT_ROLE_HIERARCHY_TYPE",
    "MAX_ROLE_HIERARCHY_DEPTH",
    "RoleHierarchyAssignmentSource",
    "RoleHierarchyType",
]
