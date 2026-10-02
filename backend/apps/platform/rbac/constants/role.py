"""
Role framework constants.

This module defines the platform-level RBAC constants used throughout
DatavionOS.

Business-domain roles (Healthcare, Laboratory, Pharmacy, Insurance, etc.)
must not be declared here. They should be registered by their respective
domains through the RBAC registry.
"""

from __future__ import annotations

from types import MappingProxyType

from django.db import models


class RoleType(
    models.TextChoices,
):
    """
    Classification of a role.
    """

    SYSTEM = (
        "system",
        "System",
    )

    ORGANIZATION = (
        "organization",
        "Organization",
    )

    CUSTOM = (
        "custom",
        "Custom",
    )


DEFAULT_ROLE_TYPE = RoleType.SYSTEM


class RoleScope(
    models.TextChoices,
):
    """
    Scope where a role is applicable.
    """

    PLATFORM = (
        "platform",
        "Platform",
    )

    ORGANIZATION = (
        "organization",
        "Organization",
    )

    FACILITY = (
        "facility",
        "Facility",
    )

    DEPARTMENT = (
        "department",
        "Department",
    )

    TEAM = (
        "team",
        "Team",
    )

    INDIVIDUAL = (
        "individual",
        "Individual",
    )


DEFAULT_ROLE_SCOPE = RoleScope.ORGANIZATION


class RoleCategory(
    models.TextChoices,
):
    """
    High-level grouping used by administration,
    reporting and UI organization.
    """

    PLATFORM = (
        "platform",
        "Platform",
    )

    MANAGEMENT = (
        "management",
        "Management",
    )

    OPERATIONS = (
        "operations",
        "Operations",
    )

    SUPPORT = (
        "support",
        "Support",
    )

    EXTERNAL = (
        "external",
        "External",
    )


DEFAULT_ROLE_CATEGORY = RoleCategory.OPERATIONS


class RoleCode:
    """
    Reserved platform role codes.

    These codes are owned by the RBAC framework and
    cannot be reused by domain modules.
    """

    #
    # Platform
    #

    PLATFORM_OWNER = "platform_owner"

    PLATFORM_ADMIN = "platform_admin"

    PLATFORM_SUPPORT = "platform_support"

    #
    # Organization
    #

    ORGANIZATION_OWNER = "organization_owner"

    ORGANIZATION_ADMIN = "organization_admin"

    ORGANIZATION_MANAGER = "organization_manager"

    #
    # Generic Business
    #

    DEPARTMENT_MANAGER = "department_manager"

    TEAM_LEAD = "team_lead"

    EMPLOYEE = "employee"

    EXTERNAL_USER = "external_user"

    READ_ONLY = "read_only"


DEFAULT_ROLE_PRIORITY = 100

DEFAULT_DISPLAY_ORDER = 100


ROLE_PRIORITIES = MappingProxyType(
    {
        RoleCode.PLATFORM_OWNER: 1000,
        RoleCode.PLATFORM_ADMIN: 900,
        RoleCode.PLATFORM_SUPPORT: 850,
        RoleCode.ORGANIZATION_OWNER: 800,
        RoleCode.ORGANIZATION_ADMIN: 700,
        RoleCode.ORGANIZATION_MANAGER: 600,
        RoleCode.DEPARTMENT_MANAGER: 500,
        RoleCode.TEAM_LEAD: 400,
        RoleCode.EMPLOYEE: 200,
        RoleCode.EXTERNAL_USER: 100,
        RoleCode.READ_ONLY: 10,
    },
)


SYSTEM_ROLE_CODES = frozenset(
    ROLE_PRIORITIES.keys(),
)


RESERVED_ROLE_CODES = SYSTEM_ROLE_CODES


RESERVED_ROLE_NAMES = frozenset(
    {
        "Platform Owner",
        "Platform Administrator",
        "Platform Support",
        "Organization Owner",
        "Organization Administrator",
        "Organization Manager",
        "Department Manager",
        "Team Lead",
        "Employee",
        "External User",
        "Read Only",
    },
)


__all__ = [
    "DEFAULT_DISPLAY_ORDER",
    "DEFAULT_ROLE_CATEGORY",
    "DEFAULT_ROLE_PRIORITY",
    "DEFAULT_ROLE_SCOPE",
    "DEFAULT_ROLE_TYPE",
    "RESERVED_ROLE_CODES",
    "RESERVED_ROLE_NAMES",
    "ROLE_PRIORITIES",
    "SYSTEM_ROLE_CODES",
    "RoleCategory",
    "RoleCode",
    "RoleScope",
    "RoleType",
]
