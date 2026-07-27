"""
Audit configuration models for DatavionOS.

Provides immutable configuration objects used by the audit
framework.

The configuration layer controls audit behaviour without
coupling to storage or compliance implementations.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class AuditConfiguration:
    """
    Audit framework configuration.

    Controls audit recording behaviour.
    """

    enabled: bool = True

    store_history: bool = True

    publish_events: bool = True

    include_request_context: bool = True

    include_actor_context: bool = True

    tenant_isolation: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class AuditRetentionConfiguration:
    """
    Audit retention configuration.

    Controls lifecycle of audit records.
    """

    retention_days: int = 2555

    archive_enabled: bool = True

    archive_after_days: int = 365


@dataclass(
    frozen=True,
    slots=True,
)
class AuditComplianceConfiguration:
    """
    Compliance-oriented audit configuration.
    """

    immutable_records: bool = True

    track_changes: bool = True

    capture_metadata: bool = True

    require_actor: bool = False


DEFAULT_AUDIT_CONFIGURATION = AuditConfiguration()


DEFAULT_AUDIT_RETENTION_CONFIGURATION = AuditRetentionConfiguration()


DEFAULT_AUDIT_COMPLIANCE_CONFIGURATION = AuditComplianceConfiguration()


__all__: tuple[str, ...] = (
    "AuditComplianceConfiguration",
    "AuditConfiguration",
    "AuditRetentionConfiguration",
    "DEFAULT_AUDIT_COMPLIANCE_CONFIGURATION",
    "DEFAULT_AUDIT_CONFIGURATION",
    "DEFAULT_AUDIT_RETENTION_CONFIGURATION",
)
