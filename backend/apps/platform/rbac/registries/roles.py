"""
Built-in role registry.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform.rbac.constants import (
    DEFAULT_ROLE_CATEGORY,
    DEFAULT_ROLE_SCOPE,
    DEFAULT_ROLE_TYPE,
    ROLE_PRIORITIES,
    RoleCode,
)


@dataclass(
    frozen=True,
    slots=True,
)
class RoleDefinition:
    """
    Immutable built-in role definition.
    """

    code: str

    name: str

    priority: int

    role_type: str = DEFAULT_ROLE_TYPE

    scope: str = DEFAULT_ROLE_SCOPE

    category: str = DEFAULT_ROLE_CATEGORY

    is_system: bool = True

    is_default: bool = False

    is_assignable: bool = True

    is_editable: bool = False

    is_deletable: bool = False


SYSTEM_ROLE_REGISTRY = (
    RoleDefinition(
        code=RoleCode.PLATFORM_OWNER,
        name="Platform Owner",
        priority=ROLE_PRIORITIES[RoleCode.PLATFORM_OWNER],
    ),
    RoleDefinition(
        code=RoleCode.PLATFORM_ADMIN,
        name="Platform Administrator",
        priority=ROLE_PRIORITIES[RoleCode.PLATFORM_ADMIN],
    ),
    RoleDefinition(
        code=RoleCode.ORGANIZATION_OWNER,
        name="Organization Owner",
        priority=ROLE_PRIORITIES[RoleCode.ORGANIZATION_OWNER],
    ),
    RoleDefinition(
        code=RoleCode.ORGANIZATION_ADMIN,
        name="Organization Administrator",
        priority=ROLE_PRIORITIES[RoleCode.ORGANIZATION_ADMIN],
    ),
    RoleDefinition(
        code=RoleCode.PLATFORM_SUPPORT,
        name="Platform Support",
        priority=ROLE_PRIORITIES[RoleCode.PLATFORM_SUPPORT],
    ),
    RoleDefinition(
        code=RoleCode.ORGANIZATION_MANAGER,
        name="Organization Manager",
        priority=ROLE_PRIORITIES[RoleCode.ORGANIZATION_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.DEPARTMENT_MANAGER,
        name="Department Manager",
        priority=ROLE_PRIORITIES[RoleCode.DEPARTMENT_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.TEAM_LEAD,
        name="Team Lead",
        priority=ROLE_PRIORITIES[RoleCode.TEAM_LEAD],
    ),
    RoleDefinition(
        code=RoleCode.EMPLOYEE,
        name="Employee",
        priority=ROLE_PRIORITIES[RoleCode.EMPLOYEE],
    ),
    RoleDefinition(
        code=RoleCode.EXTERNAL_USER,
        name="External User",
        priority=ROLE_PRIORITIES[RoleCode.EXTERNAL_USER],
    ),
    RoleDefinition(
        code=RoleCode.READ_ONLY,
        name="Read Only",
        priority=ROLE_PRIORITIES[RoleCode.READ_ONLY],
    ),
)

__all__ = [
    "RoleDefinition",
    "SYSTEM_ROLE_REGISTRY",
]
