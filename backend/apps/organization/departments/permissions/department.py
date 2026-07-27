"""
Permission classes for the Departments application.
"""

from __future__ import annotations

from apps.common.permissions.base import DatavionPermission


class CanViewDepartment(DatavionPermission):
    """
    Allows viewing departments.
    """

    required_permission = "organization.department.view"


class CanCreateDepartment(DatavionPermission):
    """
    Allows creating departments.
    """

    required_permission = "organization.department.create"


class CanUpdateDepartment(DatavionPermission):
    """
    Allows updating departments.
    """

    required_permission = "organization.department.update"


class CanDeleteDepartment(DatavionPermission):
    """
    Allows deleting departments.
    """

    required_permission = "organization.department.delete"


__all__ = (
    "CanViewDepartment",
    "CanCreateDepartment",
    "CanUpdateDepartment",
    "CanDeleteDepartment",
)
