"""
Reusable event payload models for DatavionOS.

Defines common payload structures shared across the platform
event framework.

Feature applications may extend these payloads with domain-specific
data.

Examples:

- Audit events
- User events
- Organization events
- Tenant lifecycle events
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class BaseEventPayload:
    """
    Base event payload.

    Provides a lightweight extension point for all event payloads.
    """

    data: dict[str, Any] = field(
        default_factory=dict,
    )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert payload into dictionary form.
        """

        return dict(
            self.data,
        )


@dataclass(
    frozen=True,
    slots=True,
)
class AuditEventPayload(
    BaseEventPayload,
):
    """
    Payload for audit-related events.

    Example:

        user.updated
        patient.consent_given
    """

    action: str | None = None

    resource: str | None = None

    resource_id: str | int | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class UserEventPayload(
    BaseEventPayload,
):
    """
    Payload for user lifecycle events.
    """

    user_id: str | int | None = None

    username: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class TenantEventPayload(
    BaseEventPayload,
):
    """
    Payload for tenant lifecycle events.
    """

    tenant_id: str | int | None = None

    organization_id: str | int | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class SystemEventPayload(
    BaseEventPayload,
):
    """
    Payload for platform system events.
    """

    service: str | None = None

    operation: str | None = None


__all__: tuple[str, ...] = (
    "AuditEventPayload",
    "BaseEventPayload",
    "SystemEventPayload",
    "TenantEventPayload",
    "UserEventPayload",
)
