"""
Department permission exports.
"""

from __future__ import annotations

from apps.organization.departments.permissions.department import (
    CanCreateDepartment,
    CanDeleteDepartment,
    CanUpdateDepartment,
    CanViewDepartment,
)

__all__ = [
    "CanCreateDepartment",
    "CanDeleteDepartment",
    "CanUpdateDepartment",
    "CanViewDepartment",
]
