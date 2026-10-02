from apps.billing.finance.models import FinanceAuditLog


def record_audit(
    *, organization, workflow, entity_type, entity_id=None, actor_id=None, payload=None
):
    return FinanceAuditLog.objects.create(
        organization=organization,
        workflow=workflow,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        payload=payload or {},
    )
