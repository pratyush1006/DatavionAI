"""
Department selectors.
"""

from apps.organization.departments.selectors.analytics import (
    DepartmentAnalyticsSelector,
)
from apps.organization.departments.selectors.department import (
    DepartmentSelector,
    get_active_departments,
    get_department,
    get_department_by_id,
    get_departments,
)
from apps.organization.departments.selectors.hierarchy import (
    DepartmentHierarchySelector,
)
from apps.organization.departments.selectors.members import (
    DepartmentMemberSelector,
)

__all__ = (
    "DepartmentSelector",
    "DepartmentHierarchySelector",
    "DepartmentMemberSelector",
    "DepartmentAnalyticsSelector",
    "get_departments",
    "get_department",
    "get_department_by_id",
    "get_active_departments",
)
