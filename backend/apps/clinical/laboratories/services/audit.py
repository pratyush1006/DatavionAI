from __future__ import annotations

from ..models import (
    LaboratoryAuditLog,
)


def audit(org, actor, action, entity, entity_id, metadata=None):
    return LaboratoryAuditLog.objects.create(
        organization_id=org,
        actor_id=actor,
        action=action,
        entity_type=entity,
        entity_id=entity_id,
        metadata=metadata or {},
    )
