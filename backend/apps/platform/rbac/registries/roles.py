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
        code=RoleCode.DEPARTMENT_HEAD,
        name="Department Head",
        priority=ROLE_PRIORITIES[RoleCode.DEPARTMENT_HEAD],
    ),
    RoleDefinition(
        code=RoleCode.DOCTOR,
        name="Doctor",
        priority=ROLE_PRIORITIES[RoleCode.DOCTOR],
    ),
    RoleDefinition(
        code=RoleCode.NURSE,
        name="Nurse",
        priority=ROLE_PRIORITIES[RoleCode.NURSE],
    ),
    RoleDefinition(
        code=RoleCode.RECEPTIONIST,
        name="Receptionist",
        priority=ROLE_PRIORITIES[RoleCode.RECEPTIONIST],
    ),
    RoleDefinition(
        code=RoleCode.LAB_MANAGER,
        name="Laboratory Manager",
        priority=ROLE_PRIORITIES[RoleCode.LAB_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.LAB_TECHNICIAN,
        name="Laboratory Technician",
        priority=ROLE_PRIORITIES[RoleCode.LAB_TECHNICIAN],
    ),
    RoleDefinition(
        code=RoleCode.PHARMACIST,
        name="Pharmacist",
        priority=ROLE_PRIORITIES[RoleCode.PHARMACIST],
    ),
    RoleDefinition(
        code=RoleCode.BILLING_MANAGER,
        name="Billing Manager",
        priority=ROLE_PRIORITIES[RoleCode.BILLING_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.FINANCE_MANAGER,
        name="Finance Manager",
        priority=ROLE_PRIORITIES[RoleCode.FINANCE_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.INVENTORY_MANAGER,
        name="Inventory Manager",
        priority=ROLE_PRIORITIES[RoleCode.INVENTORY_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.HR_MANAGER,
        name="HR Manager",
        priority=ROLE_PRIORITIES[RoleCode.HR_MANAGER],
    ),
    RoleDefinition(
        code=RoleCode.AUDITOR,
        name="Auditor",
        priority=ROLE_PRIORITIES[RoleCode.AUDITOR],
    ),
    RoleDefinition(
        code=RoleCode.PATIENT,
        name="Patient",
        priority=ROLE_PRIORITIES[RoleCode.PATIENT],
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
