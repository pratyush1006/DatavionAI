"""
Department models.
"""

from apps.organization.departments.models.department import (
    Department,
)
from apps.organization.departments.models.department_hierarchy import (
    DepartmentHierarchy,
)
from apps.organization.departments.models.department_member import (
    DepartmentMember,
)
from apps.organization.departments.models.department_role import (
    DepartmentRole,
)
from apps.organization.departments.models.department_setting import (
    DepartmentSetting,
)

__all__ = (
    "Department",
    "DepartmentMember",
    "DepartmentRole",
    "DepartmentSetting",
    "DepartmentHierarchy",
)
