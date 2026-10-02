from __future__ import annotations

import uuid

from django.db import transaction
from django.utils import timezone

from ..constants import OrderStatus, SpecimenStatus
from ..models import (
    LaboratoryOrder,
    LaboratorySpecimen,
)
from .audit import audit
from .events import event


@transaction.atomic
def collect_specimen(
    *, organization_id, order_id, specimen_type, collector_user_id=None, actor_id=None
):
    order = LaboratoryOrder.objects.select_for_update().get(
        id=order_id, organization_id=organization_id, is_deleted=False
    )
    now = timezone.now()
    specimen = LaboratorySpecimen.objects.create(
        organization_id=organization_id,
        order=order,
        specimen_id=f"SP-{uuid.uuid4().hex[:12].upper()}",
        accession_number=f"ACC-{uuid.uuid4().hex[:12].upper()}",
        barcode=f"LAB{uuid.uuid4().hex[:18].upper()}",
        specimen_type=specimen_type,
        status=SpecimenStatus.COLLECTED,
        collected_at=now,
        collector_user_id=collector_user_id,
        chain_of_custody=[
            {
                "event": "collected",
                "at": now.isoformat(),
                "actor_id": str(actor_id) if actor_id else None,
            }
        ],
    )
    order.status = OrderStatus.COLLECTED
    order.save(update_fields=["status", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "specimen.collected",
        "LaboratorySpecimen",
        specimen.id,
    )
    event(
        organization_id,
        "laboratory.specimen.collected",
        "LaboratorySpecimen",
        specimen.id,
    )
    return specimen
