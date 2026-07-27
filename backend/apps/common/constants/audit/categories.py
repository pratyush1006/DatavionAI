"""
DatavionAI Audit Category Constants.

Centralized audit category definitions used throughout the DatavionAI
platform.

This module defines immutable audit categories for security,
authentication, authorization, data access, administration,
configuration, workflow, integration, and operational activities.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Provider agnostic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Audit Categories
###############################################################################


class AuditCategory(StrEnum):
    """
    Standard audit categories.
    """

    AUTHENTICATION = "authentication"

    AUTHORIZATION = "authorization"

    SECURITY = "security"

    USER_MANAGEMENT = "user_management"

    ACCESS_CONTROL = "access_control"

    DATA_ACCESS = "data_access"

    DATA_MODIFICATION = "data_modification"

    CONFIGURATION = "configuration"

    ADMINISTRATION = "administration"

    SYSTEM = "system"

    WORKFLOW = "workflow"

    INTEGRATION = "integration"

    API = "api"

    NOTIFICATION = "notification"

    REPORTING = "reporting"

    COMPLIANCE = "compliance"

    BACKUP = "backup"

    MAINTENANCE = "maintenance"


SUPPORTED_AUDIT_CATEGORIES: Final[tuple[str, ...]] = tuple(
    category.value for category in AuditCategory
)

###############################################################################
# Category Groups
###############################################################################

SECURITY_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        AuditCategory.AUTHENTICATION.value,
        AuditCategory.AUTHORIZATION.value,
        AuditCategory.SECURITY.value,
        AuditCategory.ACCESS_CONTROL.value,
    }
)

DATA_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        AuditCategory.DATA_ACCESS.value,
        AuditCategory.DATA_MODIFICATION.value,
    }
)

SYSTEM_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        AuditCategory.SYSTEM.value,
        AuditCategory.CONFIGURATION.value,
        AuditCategory.ADMINISTRATION.value,
        AuditCategory.MAINTENANCE.value,
        AuditCategory.BACKUP.value,
    }
)

BUSINESS_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        AuditCategory.WORKFLOW.value,
        AuditCategory.REPORTING.value,
        AuditCategory.NOTIFICATION.value,
        AuditCategory.INTEGRATION.value,
        AuditCategory.API.value,
    }
)

GOVERNANCE_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        AuditCategory.COMPLIANCE.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "AuditCategory",
)
