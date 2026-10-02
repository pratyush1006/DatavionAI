"""
Department permission exports.
"""

from __future__ import annotations

from apps.organization.departments.permissions.department import (
    CanActivateDepartment,
    CanApproveDepartment,
    CanAssignDepartmentMember,
    CanCreateDepartment,
    CanDeactivateDepartment,
    CanDeleteDepartment,
    CanUpdateDepartment,
    CanViewDepartment,
)

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
