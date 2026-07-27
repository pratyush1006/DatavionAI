"""
Audit services for DatavionOS.

Provides the application service layer for audit operations.

Business applications should use this service instead of
directly accessing the recorder or registry.
"""

from __future__ import annotations

from apps.common.audit.models import (
    AuditRecord,
    AuditResult,
)
from apps.common.audit.recorder import (
    audit_recorder,
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


class AuditService:
    """
    Audit application service.

    Provides:

    - Audit record creation
    - Audit record processing
    """

    def create(
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

        return audit_recorder.create_record(
            action=action,
            resource=resource,
            resource_id=resource_id,
            actor_id=actor_id,
            category=category,
            tenant_id=tenant_id,
            organization_id=organization_id,
            context=context,
            metadata=metadata,
        )

    def record(
        self,
        audit_record: AuditRecord,
    ) -> AuditResult:
        """
        Process an audit record.
        """

        return audit_recorder.record(
            audit_record,
        )


audit_service = AuditService()


__all__: tuple[str, ...] = (
    "AuditService",
    "audit_service",
)
