from django.db import transaction

from ..constants import ResultStatus
from ..models import LaboratoryResult
from .audit import audit
from .events import event
from .laboratory import LaboratoryServiceError


@transaction.atomic
def validate_result_for_verification(*, organization_id, result_id, actor_id=None):
    result = LaboratoryResult.objects.select_for_update().get(
        id=result_id, organization_id=organization_id, is_deleted=False
    )
    if result.status not in {ResultStatus.PRELIMINARY, ResultStatus.CORRECTED}:
        raise LaboratoryServiceError(
            "Result is not eligible for compliance validation."
        )
    if result.value_numeric is None and not result.value_text.strip():
        raise LaboratoryServiceError(
            "A laboratory result requires a numeric or text value."
        )
    if result.critical and result.abnormal_flag not in {
        "critical_low",
        "critical_high",
        "abnormal",
    }:
        raise LaboratoryServiceError(
            "Critical results require a critical or abnormal flag."
        )
    audit(
        organization_id,
        actor_id,
        "result.compliance_validated",
        "LaboratoryResult",
        result.id,
    )
    event(
        organization_id,
        "laboratory.result.compliance_validated",
        "LaboratoryResult",
        result.id,
    )
    return result
