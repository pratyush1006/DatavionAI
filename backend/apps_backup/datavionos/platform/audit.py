"""
Platform audit contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class AuditSeverity(
    StrEnum,
):
    """
    Audit severity.
    """

    INFORMATION = "information"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(
    frozen=True,
    slots=True,
)
class AuditRecord:
    """
    Immutable audit record.
    """

    action: str

    resource_type: str

    resource_id: str

    timestamp: datetime

    severity: AuditSeverity

    tenant_id: str | None = None

    organization_id: str | None = None

    user_id: str | None = None

    correlation_id: str | None = None

    request_id: str | None = None

    outcome: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class AuditService(
    Protocol,
):
    """
    Platform audit abstraction.
    """

    def record(
        self,
        audit_record: AuditRecord,
    ) -> None:
        """
        Persist an immutable audit record.
        """

    def record_action(
        self,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        severity: AuditSeverity = AuditSeverity.INFORMATION,
        tenant_id: str | None = None,
        organization_id: str | None = None,
        user_id: str | None = None,
        correlation_id: str | None = None,
        request_id: str | None = None,
        outcome: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Record an audit event.
        """


__all__ = [
    "AuditSeverity",
    "AuditRecord",
    "AuditService",
]
