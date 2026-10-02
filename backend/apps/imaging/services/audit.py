from apps.imaging.models import ImagingAuditEvent


def record_event(
    *, tenant_id, event_type, entity_type, entity_id, actor_id=None, payload=None
):
    return ImagingAuditEvent.objects.create(
        tenant_id=tenant_id,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        payload=payload or {},
    )
