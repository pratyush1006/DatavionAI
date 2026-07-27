"""
DatavionAI Audit Level Constants.

Centralized audit severity levels used throughout the DatavionAI
platform.

This module defines immutable audit severity levels for security,
compliance, monitoring, and operational events.

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
# Audit Severity Levels
###############################################################################


class AuditLevel(StrEnum):
    """
    Standard audit severity levels.
    """

    TRACE = "trace"

    DEBUG = "debug"

    INFO = "info"

    NOTICE = "notice"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"

    ALERT = "alert"

    EMERGENCY = "emergency"


SUPPORTED_AUDIT_LEVELS: Final[tuple[str, ...]] = tuple(
    level.value for level in AuditLevel
)

###############################################################################
# Level Priorities
###############################################################################

LEVEL_PRIORITY_TRACE: Final[int] = 10

LEVEL_PRIORITY_DEBUG: Final[int] = 20

LEVEL_PRIORITY_INFO: Final[int] = 30

LEVEL_PRIORITY_NOTICE: Final[int] = 40

LEVEL_PRIORITY_WARNING: Final[int] = 50

LEVEL_PRIORITY_ERROR: Final[int] = 60

LEVEL_PRIORITY_CRITICAL: Final[int] = 70

LEVEL_PRIORITY_ALERT: Final[int] = 80

LEVEL_PRIORITY_EMERGENCY: Final[int] = 90

###############################################################################
# Severity Groups
###############################################################################

LOW_SEVERITY_LEVELS: Final[frozenset[str]] = frozenset(
    {
        AuditLevel.TRACE.value,
        AuditLevel.DEBUG.value,
        AuditLevel.INFO.value,
        AuditLevel.NOTICE.value,
    }
)

MEDIUM_SEVERITY_LEVELS: Final[frozenset[str]] = frozenset(
    {
        AuditLevel.WARNING.value,
    }
)

HIGH_SEVERITY_LEVELS: Final[frozenset[str]] = frozenset(
    {
        AuditLevel.ERROR.value,
        AuditLevel.CRITICAL.value,
    }
)

EMERGENCY_SEVERITY_LEVELS: Final[frozenset[str]] = frozenset(
    {
        AuditLevel.ALERT.value,
        AuditLevel.EMERGENCY.value,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "AuditLevel",
    "SUPPORTED_AUDIT_LEVELS",
    "LEVEL_PRIORITY_TRACE",
    "LEVEL_PRIORITY_DEBUG",
    "LEVEL_PRIORITY_INFO",
    "LEVEL_PRIORITY_NOTICE",
    "LEVEL_PRIORITY_WARNING",
    "LEVEL_PRIORITY_ERROR",
    "LEVEL_PRIORITY_CRITICAL",
    "LEVEL_PRIORITY_ALERT",
    "LEVEL_PRIORITY_EMERGENCY",
    "LOW_SEVERITY_LEVELS",
    "MEDIUM_SEVERITY_LEVELS",
    "HIGH_SEVERITY_LEVELS",
    "EMERGENCY_SEVERITY_LEVELS",
)
