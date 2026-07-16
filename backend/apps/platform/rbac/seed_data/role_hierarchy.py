"""
Built-in RBAC role hierarchy.
"""

from __future__ import annotations

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE,
    DEFAULT_ROLE_HIERARCHY_TYPE,
    SystemRole,
)

ROLE_HIERARCHY = (
    #
    # Platform
    #
    {
        "parent_role": SystemRole.PLATFORM_ADMIN.value,
        "child_role": SystemRole.ORGANIZATION_OWNER.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    #
    # Organization
    #
    {
        "parent_role": SystemRole.ORGANIZATION_OWNER.value,
        "child_role": SystemRole.ORGANIZATION_ADMIN.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    #
    # Clinical
    #
    {
        "parent_role": SystemRole.ORGANIZATION_ADMIN.value,
        "child_role": SystemRole.DOCTOR.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    {
        "parent_role": SystemRole.DOCTOR.value,
        "child_role": SystemRole.CONSULTANT.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    {
        "parent_role": SystemRole.DOCTOR.value,
        "child_role": SystemRole.NURSE.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    #
    # Laboratory
    #
    {
        "parent_role": (SystemRole.LABORATORY_MANAGER.value),
        "child_role": (SystemRole.LABORATORY_TECHNICIAN.value),
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    #
    # Pharmacy
    #
    {
        "parent_role": SystemRole.ORGANIZATION_ADMIN.value,
        "child_role": SystemRole.PHARMACIST.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
    #
    # Front Office
    #
    {
        "parent_role": SystemRole.ORGANIZATION_ADMIN.value,
        "child_role": SystemRole.RECEPTIONIST.value,
        "hierarchy_type": DEFAULT_ROLE_HIERARCHY_TYPE,
        "assignment_source": (DEFAULT_ROLE_HIERARCHY_ASSIGNMENT_SOURCE),
    },
)

__all__ = [
    "ROLE_HIERARCHY",
]
