"""
Department business services.
"""

from __future__ import annotations

from apps.organization.departments.services.department import (
    DepartmentService,
    create_department,
    delete_department,
    update_department,
)

__all__ = [
    "DepartmentService",
    "create_department",
    "update_department",
    "delete_department",
]
