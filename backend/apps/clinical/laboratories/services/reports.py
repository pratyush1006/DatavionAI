from __future__ import annotations

import uuid

from django.db import transaction
from django.utils import timezone

from apps.clinical.appointments.services import AppointmentService

from ..constants import OrderStatus, ResultStatus
from ..models import (
    LaboratoryOrder,
    LaboratoryReport,
)
from .audit import audit
from .events import event
from .laboratory import LaboratoryServiceError


@transaction.atomic
def release_report(*, organization_id, order_id, actor_id=None):
    order = LaboratoryOrder.objects.prefetch_related(
        "items__result", "items__test"
    ).get(id=order_id, organization_id=organization_id, is_deleted=False)
    rows = []
    for item in order.items.all():
        result = getattr(item, "result", None)
        if not result or result.status != ResultStatus.FINAL:
            raise LaboratoryServiceError("Every ordered test requires a final result.")
        rows.append(
            {
                "test_code": item.test.code,
                "test_name": item.test.name,
                "value_numeric": (
                    str(result.value_numeric)
                    if result.value_numeric is not None
                    else None
                ),
                "value_text": result.value_text,
                "unit": result.unit,
                "reference_range": result.reference_range,
                "abnormal_flag": result.abnormal_flag,
                "critical": result.critical,
                "comments": result.comments,
            }
        )
    report, _ = LaboratoryReport.objects.get_or_create(
        order=order,
        defaults={
            "organization_id": organization_id,
            "report_number": f"RPT-{uuid.uuid4().hex[:12].upper()}",
        },
    )
    now = timezone.now()
    report.status = "released"
    report.report_data = {
        "order_number": order.order_number,
        "released_at": now.isoformat(),
        "results": rows,
    }
    report.verified_by_id = actor_id
    report.released_at = now
    report.save()
    order.status = OrderStatus.RELEASED
    order.save(update_fields=["status", "updated_at"])
    for item in order.items.all():
        item.result.released_at = now
        item.result.save(update_fields=["released_at", "updated_at"])
    audit(organization_id, actor_id, "report.released", "LaboratoryReport", report.id)
    event(organization_id, "laboratory.report.released", "LaboratoryReport", report.id)
    return report


__all__ = (
    "LaboratoryServiceError",
    "allocate_slot_for_appointment",
    "release_slot_for_appointment",
    "create_order",
    "collect_specimen",
    "enter_result",
    "verify_result",
    "release_report",
    "AppointmentService",
)
