from django.db import transaction
from django.utils import timezone

from apps.imaging.constants.choices import ContrastStatus
from apps.imaging.models import ContrastAssessment
from apps.imaging.services.audit import record_event


class CECTWorkflowError(ValueError):
    pass


@transaction.atomic
def clear_contrast(*, assessment_id, tenant_id, assessed_by_id):
    assessment = ContrastAssessment.objects.select_for_update().get(
        id=assessment_id, tenant_id=tenant_id
    )
    if assessment.status != ContrastStatus.SCREENING:
        raise CECTWorkflowError("Contrast assessment is not in screening state.")
    if not all(
        (
            assessment.allergy_screened,
            assessment.renal_screened,
            assessment.pregnancy_screened,
        )
    ):
        raise CECTWorkflowError("Required configured screening checks are incomplete.")
    assessment.status = ContrastStatus.CLEARED
    assessment.assessed_by_id = assessed_by_id
    assessment.assessed_at = timezone.now()
    assessment.full_clean()
    assessment.save(
        update_fields=["status", "assessed_by_id", "assessed_at", "updated_at"]
    )
    record_event(
        tenant_id=tenant_id,
        event_type="contrast.cleared",
        entity_type="ContrastAssessment",
        entity_id=assessment.id,
        actor_id=assessed_by_id,
    )
    return assessment


@transaction.atomic
def record_contrast_administration(
    *, assessment_id, tenant_id, administration_reference="", actor_id=None
):
    assessment = ContrastAssessment.objects.select_for_update().get(
        id=assessment_id, tenant_id=tenant_id
    )
    if assessment.status != ContrastStatus.CLEARED:
        raise CECTWorkflowError("Contrast must be cleared before administration.")
    assessment.status = ContrastStatus.ADMINISTERED
    assessment.administration_reference = administration_reference
    assessment.administered_at = timezone.now()
    assessment.save(
        update_fields=[
            "status",
            "administration_reference",
            "administered_at",
            "updated_at",
        ]
    )
    record_event(
        tenant_id=tenant_id,
        event_type="contrast.administered",
        entity_type="ContrastAssessment",
        entity_id=assessment.id,
        actor_id=actor_id,
    )
    return assessment
