"""
DatavionAI Audit Resource Constants.

Centralized audit resource definitions used throughout the DatavionAI
platform.

This module defines immutable audit resources representing the platform
objects that can be audited.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- Platform-wide resources only
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Audit Resources
###############################################################################


class AuditResource(StrEnum):
    """
    Standard audit resources.
    """

    # Platform
    APPLICATION = "application"
    PLATFORM = "platform"
    SYSTEM = "system"

    # Identity & Access Management
    USER = "user"
    ROLE = "role"
    PERMISSION = "permission"
    GROUP = "group"
    SESSION = "session"

    # Organization
    ORGANIZATION = "organization"
    TENANT = "tenant"
    DEPARTMENT = "department"
    TEAM = "team"
    LOCATION = "location"

    # Configuration
    CONFIGURATION = "configuration"
    SETTING = "setting"
    FEATURE_FLAG = "feature_flag"

    # Security
    API_KEY = "api_key"
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    CERTIFICATE = "certificate"

    # Workflow
    WORKFLOW = "workflow"
    TASK = "task"
    JOB = "job"

    # Communication
    NOTIFICATION = "notification"
    WEBHOOK = "webhook"

    # Storage
    FILE = "file"
    DOCUMENT = "document"

    # Integration
    INTEGRATION = "integration"

    # Healthcare (platform-wide)
    PATIENT = "patient"
    PRACTITIONER = "practitioner"
    APPOINTMENT = "appointment"
    ENCOUNTER = "encounter"
    OBSERVATION = "observation"
    MEDICATION = "medication"
    PRESCRIPTION = "prescription"
    LABORATORY_ORDER = "laboratory_order"
    LABORATORY_RESULT = "laboratory_result"
    IMAGING_ORDER = "imaging_order"
    IMAGING_RESULT = "imaging_result"
    INVOICE = "invoice"
    PAYMENT = "payment"


SUPPORTED_AUDIT_RESOURCES: Final[tuple[str, ...]] = tuple(
    resource.value for resource in AuditResource
)

###############################################################################
# Resource Groups
###############################################################################

IDENTITY_RESOURCES: Final[frozenset[str]] = frozenset(
    {
        AuditResource.USER.value,
        AuditResource.ROLE.value,
        AuditResource.PERMISSION.value,
        AuditResource.GROUP.value,
        AuditResource.SESSION.value,
    }
)

ORGANIZATION_RESOURCES: Final[frozenset[str]] = frozenset(
    {
        AuditResource.ORGANIZATION.value,
        AuditResource.TENANT.value,
        AuditResource.DEPARTMENT.value,
        AuditResource.TEAM.value,
        AuditResource.LOCATION.value,
    }
)

SECURITY_RESOURCES: Final[frozenset[str]] = frozenset(
    {
        AuditResource.API_KEY.value,
        AuditResource.ACCESS_TOKEN.value,
        AuditResource.REFRESH_TOKEN.value,
        AuditResource.CERTIFICATE.value,
    }
)

WORKFLOW_RESOURCES: Final[frozenset[str]] = frozenset(
    {
        AuditResource.WORKFLOW.value,
        AuditResource.TASK.value,
        AuditResource.JOB.value,
    }
)

HEALTHCARE_RESOURCES: Final[frozenset[str]] = frozenset(
    {
        AuditResource.PATIENT.value,
        AuditResource.PRACTITIONER.value,
        AuditResource.APPOINTMENT.value,
        AuditResource.ENCOUNTER.value,
        AuditResource.OBSERVATION.value,
        AuditResource.MEDICATION.value,
        AuditResource.PRESCRIPTION.value,
        AuditResource.LABORATORY_ORDER.value,
        AuditResource.LABORATORY_RESULT.value,
        AuditResource.IMAGING_ORDER.value,
        AuditResource.IMAGING_RESULT.value,
        AuditResource.INVOICE.value,
        AuditResource.PAYMENT.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "AuditResource",
)
