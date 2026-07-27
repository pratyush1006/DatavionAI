"""
Audit models for DatavionOS.

Defines immutable framework-level audit objects.

These models describe audit mechanics only.

Business-specific audit rules belong to domain applications:

- patients
- laboratories
- billing
- clinical
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)

from apps.common.audit.constants import (
    DEFAULT_CATEGORY,
    DEFAULT_LEVEL,
)
from apps.common.audit.types import (
    ActorID,
    AuditAction,
    AuditCategory,
    AuditContext,
    AuditID,
    AuditMetadata,
    AuditResource,
    OrganizationID,
    TenantID,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AuditActor:
    """
    Represents the actor responsible for an action.
    """

    actor_id: ActorID = None

    username: str | None = None

    metadata: AuditMetadata = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class AuditChange:
    """
    Represents before/after data changes.
    """

    field_name: str

    old_value: object | None = None

    new_value: object | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class AuditRecord:
    """
    Immutable audit record.

    Represents a single auditable action.
    """

    audit_id: AuditID

    action: AuditAction

    resource: AuditResource

    actor: AuditActor = field(
        default_factory=AuditActor,
    )

    category: AuditCategory = DEFAULT_CATEGORY

    level: str = DEFAULT_LEVEL

    resource_id: str | int | None = None

    tenant_id: TenantID = None

    organization_id: OrganizationID = None

    changes: tuple[AuditChange, ...] = ()

    context: AuditContext = field(
        default_factory=dict,
    )

    metadata: AuditMetadata = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class AuditResult:
    """
    Result returned after audit processing.
    """

    success: bool

    audit_id: AuditID

    message: str = ""

    metadata: AuditMetadata = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "AuditActor",
    "AuditChange",
    "AuditRecord",
    "AuditResult",
)
