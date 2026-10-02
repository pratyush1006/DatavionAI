from django.db import transaction
from django.utils import timezone

from ..constants import ResultStatus
from ..models import LaboratoryOrderItem, LaboratoryResult
from .audit import audit
from .compliance import validate_result_for_verification
from .events import event
from .laboratory import LaboratoryServiceError


@transaction.atomic
def enter_result(
    *,
    organization_id,
    order_item_id,
    value_numeric=None,
    value_text="",
    unit="",
    reference_range=None,
    abnormal_flag="normal",
    critical=False,
    comments="",
    actor_id=None,
):
    item = (
        LaboratoryOrderItem.objects.select_related("order", "test")
        .select_for_update()
        .get(id=order_item_id, order__organization_id=organization_id, is_deleted=False)
    )
    if item.order.status == "cancelled":
        raise LaboratoryServiceError("Results cannot be entered for a cancelled order.")
    result, _ = LaboratoryResult.objects.get_or_create(
        order_item=item,
        defaults={
            "organization_id": organization_id,
            "unit": unit or item.test.unit,
            "reference_range": reference_range or item.test.reference_range,
        },
    )
    result.value_numeric = value_numeric
    result.value_text = value_text
    result.unit = unit or item.test.unit
    result.reference_range = reference_range or item.test.reference_range
    result.abnormal_flag = abnormal_flag
    result.critical = critical
    result.comments = comments
    result.status = ResultStatus.PRELIMINARY
    result.entered_by_id = actor_id
    result.entered_at = timezone.now()
    result.save()
    item.status = "processing"
    item.save(update_fields=["status", "updated_at"])
    audit(organization_id, actor_id, "result.entered", "LaboratoryResult", result.id)
    event(
        organization_id,
        "laboratory.result.critical" if critical else "laboratory.result.entered",
        "LaboratoryResult",
        result.id,
    )
    return result


@transaction.atomic
def verify_result(*, organization_id, result_id, actor_id=None):
    result = validate_result_for_verification(
        organization_id=organization_id, result_id=result_id, actor_id=actor_id
    )
    result = LaboratoryResult.objects.select_for_update().get(
        id=result.id, organization_id=organization_id, is_deleted=False
    )
    result.status = ResultStatus.FINAL
    result.verified_by_id = actor_id
    result.verified_at = timezone.now()
    result.save(update_fields=["status", "verified_by_id", "verified_at", "updated_at"])
    result.order_item.status = "verified"
    result.order_item.save(update_fields=["status", "updated_at"])
    audit(organization_id, actor_id, "result.verified", "LaboratoryResult", result.id)
    event(organization_id, "laboratory.result.verified", "LaboratoryResult", result.id)
    return result
