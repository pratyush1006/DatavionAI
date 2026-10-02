from apps.pharmacy.models import PharmacyAuditLog


def record_audit(
    *, organization, action, entity_type, entity_id=None, actor_id=None, payload=None
):
    return PharmacyAuditLog.objects.create(
        organization=organization,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=getattr(actor_id, "pk", actor_id) if actor_id else None,
        payload=payload or {},
    )
