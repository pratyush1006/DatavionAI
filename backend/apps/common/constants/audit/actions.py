"""
DatavionAI Audit Action Constants.

Centralized audit action definitions used throughout the DatavionAI
platform.

This module defines immutable audit actions for entity lifecycle,
authentication, authorization, workflow, data management, and
administrative operations.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Audit Actions
###############################################################################


class AuditAction(StrEnum):
    """
    Standard audit actions.
    """

    # Entity Lifecycle
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    RESTORE = "restore"
    ARCHIVE = "archive"
    UNARCHIVE = "unarchive"

    # Read Operations
    VIEW = "view"
    LIST = "list"
    SEARCH = "search"
    EXPORT = "export"
    IMPORT = "import"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    PRINT = "print"

    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"

    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"

    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    MFA_VERIFIED = "mfa_verified"

    # Authorization
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"

    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_REVOKED = "permission_revoked"

    ROLE_ASSIGNED = "role_assigned"
    ROLE_REMOVED = "role_removed"

    # Workflow
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"

    APPROVE = "approve"
    REJECT = "reject"

    ASSIGN = "assign"
    UNASSIGN = "unassign"

    # Configuration
    ENABLE = "enable"
    DISABLE = "disable"

    CONFIGURE = "configure"

    # Integration
    SYNCHRONIZE = "synchronize"

    CONNECT = "connect"
    DISCONNECT = "disconnect"

    # System
    BACKUP = "backup"
    RESTORE_BACKUP = "restore_backup"

    DEPLOY = "deploy"
    ROLLBACK = "rollback"


SUPPORTED_AUDIT_ACTIONS: Final[tuple[str, ...]] = tuple(
    action.value for action in AuditAction
)

###############################################################################
# Action Groups
###############################################################################

ENTITY_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.CREATE.value,
        AuditAction.UPDATE.value,
        AuditAction.DELETE.value,
        AuditAction.RESTORE.value,
        AuditAction.ARCHIVE.value,
        AuditAction.UNARCHIVE.value,
    }
)

READ_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.VIEW.value,
        AuditAction.LIST.value,
        AuditAction.SEARCH.value,
        AuditAction.EXPORT.value,
        AuditAction.DOWNLOAD.value,
        AuditAction.PRINT.value,
    }
)

AUTHENTICATION_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.LOGIN.value,
        AuditAction.LOGOUT.value,
        AuditAction.LOGIN_FAILED.value,
        AuditAction.PASSWORD_CHANGE.value,
        AuditAction.PASSWORD_RESET.value,
        AuditAction.MFA_ENABLED.value,
        AuditAction.MFA_DISABLED.value,
        AuditAction.MFA_VERIFIED.value,
    }
)

AUTHORIZATION_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.ACCESS_GRANTED.value,
        AuditAction.ACCESS_DENIED.value,
        AuditAction.PERMISSION_GRANTED.value,
        AuditAction.PERMISSION_REVOKED.value,
        AuditAction.ROLE_ASSIGNED.value,
        AuditAction.ROLE_REMOVED.value,
    }
)

WORKFLOW_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.START.value,
        AuditAction.STOP.value,
        AuditAction.PAUSE.value,
        AuditAction.RESUME.value,
        AuditAction.APPROVE.value,
        AuditAction.REJECT.value,
        AuditAction.ASSIGN.value,
        AuditAction.UNASSIGN.value,
    }
)

SYSTEM_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        AuditAction.BACKUP.value,
        AuditAction.RESTORE_BACKUP.value,
        AuditAction.DEPLOY.value,
        AuditAction.ROLLBACK.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "AuditAction",
)
