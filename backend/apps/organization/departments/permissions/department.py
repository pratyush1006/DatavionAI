"""
Department RBAC permissions.

Department bounded context permission adapters.

Uses the DatavionOS centralized RBAC engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewDepartment(
    RBACPermissionBase,
):
    """
    Allows viewing departments.
    """

    message = "You do not have permission to view departments."

    permission_code = "departments.view"


class CanCreateDepartment(
    RBACPermissionBase,
):
    """
    Allows creating departments.
    """

    message = "You do not have permission to create departments."

    permission_code = "departments.create"


class CanUpdateDepartment(
    RBACPermissionBase,
):
    """
    Allows updating departments.
    """

    message = "You do not have permission to update departments."

    permission_code = "departments.update"


class CanDeleteDepartment(
    RBACPermissionBase,
):
    """
    Allows deleting departments.
    """

    message = "You do not have permission to delete departments."

    permission_code = "departments.delete"


class CanActivateDepartment(
    RBACPermissionBase,
):
    """
    Allows activating departments.
    """

    message = "You do not have permission to activate departments."

    permission_code = "departments.activate"


class CanDeactivateDepartment(
    RBACPermissionBase,
):
    """
    Allows deactivating departments.
    """

    message = "You do not have permission to deactivate departments."

    permission_code = "departments.deactivate"


class CanAssignDepartmentMember(
    RBACPermissionBase,
):
    """
    Allows assigning members to departments.
    """

    message = "You do not have permission to assign department members."

    permission_code = "departments.assign"


class CanApproveDepartment(
    RBACPermissionBase,
):
    """
    Allows approving department operations.
    """

    message = "You do not have permission to approve department operations."

    permission_code = "departments.approve"


__all__ = (
    "CanViewDepartment",
    "CanCreateDepartment",
    "CanUpdateDepartment",
    "CanDeleteDepartment",
    "CanActivateDepartment",
    "CanDeactivateDepartment",
    "CanAssignDepartmentMember",
    "CanApproveDepartment",
)
