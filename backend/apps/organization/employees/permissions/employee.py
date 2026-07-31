"""
Employee RBAC permissions.

Employee bounded context permission adapters.

Uses the DatavionOS centralized RBAC engine.

Permission naming convention:

    <module>.<action>

Examples:

    employees.view
    employees.create
    employees.assign
    employees.contract
    employees.onboard
    employees.offboard

Architecture:

API Permission Class
        |
RBACPermissionBase
        |
DatavionOS RBAC Engine
        |
RolePermission
        |
OrganizationRole
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewEmployee(
    RBACPermissionBase,
):
    """
    Allows viewing employees.
    """

    message = "You do not have permission to view employees."

    permission_code = "employees.view"


class CanCreateEmployee(
    RBACPermissionBase,
):
    """
    Allows creating employees.
    """

    message = "You do not have permission to create employees."

    permission_code = "employees.create"


class CanUpdateEmployee(
    RBACPermissionBase,
):
    """
    Allows updating employees.
    """

    message = "You do not have permission to update employees."

    permission_code = "employees.update"


class CanDeleteEmployee(
    RBACPermissionBase,
):
    """
    Allows deleting employees.
    """

    message = "You do not have permission to delete employees."

    permission_code = "employees.delete"


class CanActivateEmployee(
    RBACPermissionBase,
):
    """
    Allows activating employees.

    Permission:

        employees.activate
    """

    message = "You do not have permission to activate employees."

    permission_code = "employees.activate"


class CanDeactivateEmployee(
    RBACPermissionBase,
):
    """
    Allows deactivating employees.

    Permission:

        employees.deactivate
    """

    message = "You do not have permission to deactivate employees."

    permission_code = "employees.deactivate"


class CanAssignEmployee(
    RBACPermissionBase,
):
    """
    Allows assigning employees.

    Permission:

        employees.assign
    """

    message = "You do not have permission to assign employees."

    permission_code = "employees.assign"


class CanManageEmployeeContracts(
    RBACPermissionBase,
):
    """
    Allows managing employee contracts.

    Permission:

        employees.contract

    Used by:

    - Employee contract management workflow
    - Contract update lifecycle
    - HR operations
    """

    message = "You do not have permission to manage employee contracts."

    permission_code = "employees.contract"


class CanOnboardEmployee(
    RBACPermissionBase,
):
    """
    Allows onboarding employees.

    Permission:

        employees.onboard
    """

    message = "You do not have permission to onboard employees."

    permission_code = "employees.onboard"


class CanOffboardEmployee(
    RBACPermissionBase,
):
    """
    Allows offboarding employees.

    Permission:

        employees.offboard
    """

    message = "You do not have permission to offboard employees."

    permission_code = "employees.offboard"


__all__ = (
    "CanViewEmployee",
    "CanCreateEmployee",
    "CanUpdateEmployee",
    "CanDeleteEmployee",
    "CanActivateEmployee",
    "CanDeactivateEmployee",
    "CanAssignEmployee",
    "CanManageEmployeeContracts",
    "CanOnboardEmployee",
    "CanOffboardEmployee",
)
