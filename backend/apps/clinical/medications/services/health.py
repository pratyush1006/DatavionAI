from apps.clinical.medications.models import Medication, MedicationOutboxEvent


def health_summary():
    return {
        "medications": Medication.objects.filter(is_deleted=False).count(),
        "pending_events": MedicationOutboxEvent.objects.filter(
            status=MedicationOutboxEvent.Status.PENDING
        ).count(),
        "failed_events": MedicationOutboxEvent.objects.filter(
            status=MedicationOutboxEvent.Status.FAILED
        ).count(),
    }
