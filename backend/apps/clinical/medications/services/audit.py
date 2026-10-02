from apps.clinical.medications.models import MedicationAuditLog


def record_audit(*, organization, medication, action, actor=None, payload=None):
    return MedicationAuditLog.objects.create(
        organization=organization,
        medication=medication,
        actor_id=getattr(actor, "id", None),
        action=str(action),
        payload=payload or {},
    )
