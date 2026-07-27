"""
Audit enumerations for the DatavionOS platform.

Defines standardized audit actions, categories,
outcomes and severity levels.
"""

from __future__ import annotations

from enum import StrEnum


class AuditAction(StrEnum):
    """
    Supported audit actions.
    """

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RESTORE = "restore"

    VIEW = "view"
    ACCESS = "access"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    EXPORT = "export"
    IMPORT = "import"

    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLE = "mfa_enable"

    APPROVE = "approve"
    REJECT = "reject"

    AI_INFERENCE = "ai_inference"

    CONFIG_UPDATE = "config_update"
    PERMISSION_CHANGE = "permission_change"

    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"


class AuditCategory(StrEnum):
    """
    Audit event categories.
    """

    SECURITY = "security"

    USER = "user"

    ORGANIZATION = "organization"

    TENANT = "tenant"

    PATIENT = "patient"

    CLINICAL = "clinical"

    DOCUMENT = "document"

    BILLING = "billing"

    AI = "ai"

    INTEGRATION = "integration"

    SYSTEM = "system"


class AuditOutcome(StrEnum):
    """
    Audit operation result.
    """

    SUCCESS = "success"

    FAILURE = "failure"

    DENIED = "denied"


class AuditSeverity(StrEnum):
    """
    Audit event severity.
    """

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


__all__ = [
    "AuditAction",
    "AuditCategory",
    "AuditOutcome",
    "AuditSeverity",
]
