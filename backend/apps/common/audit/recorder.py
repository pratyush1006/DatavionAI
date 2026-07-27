"""
Audit recorder for DatavionOS.

Provides the core audit recording engine.

Responsibilities:

- Create audit records
- Generate audit identifiers
- Dispatch records to registered handlers
- Return audit processing results

Storage persistence is intentionally delegated to handlers.
"""

from __future__ import annotations

from uuid import uuid4

from apps.common.audit.exceptions import (
    AuditRecordingError,
)
from apps.common.audit.models import (
    AuditActor,
    AuditRecord,
    AuditResult,
)
from apps.common.audit.registry import (
    audit_registry,
)
from apps.common.audit.types import (
    ActorID,
    AuditAction,
    AuditCategory,
    AuditContext,
    AuditMetadata,
    AuditResource,
    OrganizationID,
    TenantID,
)


class AuditRecorder:
    """
    Core audit recording engine.
    """

    def create_record(
        self,
        *,
        action: AuditAction,
        resource: AuditResource,
        resource_id: str | int | None = None,
        actor_id: ActorID = None,
        category: AuditCategory | None = None,
        tenant_id: TenantID = None,
        organization_id: OrganizationID = None,
        context: AuditContext | None = None,
        metadata: AuditMetadata | None = None,
    ) -> AuditRecord:
        """
        Create an audit record.
        """

        return AuditRecord(
            audit_id=str(
                uuid4(),
            ),
            action=action,
            resource=resource,
            resource_id=resource_id,
            actor=AuditActor(
                actor_id=actor_id,
            ),
            category=(category if category is not None else "system"),
            tenant_id=tenant_id,
            organization_id=organization_id,
            context=context or {},
            metadata=metadata or {},
        )

    def record(
        self,
        audit_record: AuditRecord,
    ) -> AuditResult:
        """
        Process an audit record.

        Registered handlers receive the record.
        """

        try:
            for handler in audit_registry.all():
                handler.handle(
                    audit_record,
                )

            return AuditResult(
                success=True,
                audit_id=audit_record.audit_id,
                message="Audit record processed.",
            )

        except Exception as exc:
            raise AuditRecordingError(
                str(exc),
            ) from exc


audit_recorder = AuditRecorder()


__all__: tuple[str, ...] = (
    "AuditRecorder",
    "audit_recorder",
)
