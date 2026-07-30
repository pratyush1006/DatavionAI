"""
Department services.

Public service API for Departments bounded context.
"""

from apps.organization.departments.services.department import (
    DepartmentService,
    create_department,
    delete_department,
    update_department,
)
from apps.organization.departments.services.hierarchy import (
    DepartmentHierarchyService,
)
from apps.organization.departments.services.member import (
    DepartmentMemberService,
)
from apps.organization.departments.services.role import (
    DepartmentRoleService,
)
from apps.organization.departments.services.settings import (
    DepartmentSettingsService,
)

__all__ = (
    "DepartmentService",
    "DepartmentMemberService",
    "DepartmentRoleService",
    "DepartmentHierarchyService",
    "DepartmentSettingsService",
    "create_department",
    "update_department",
    "delete_department",
)
