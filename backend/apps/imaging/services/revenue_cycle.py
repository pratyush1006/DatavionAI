from django.db import transaction

from apps.imaging.constants.choices import ChargeStatus
from apps.imaging.models import ImagingChargeLink
from apps.imaging.services.audit import record_event


@transaction.atomic
def link_charge(
    *, study_id, charge_id, procedure_code, tenant_id, idempotency_key, actor_id=None
):
    link, created = ImagingChargeLink.objects.get_or_create(
        tenant_id=tenant_id,
        idempotency_key=idempotency_key,
        defaults={
            "study_id": study_id,
            "charge_id": charge_id,
            "procedure_code": procedure_code,
            "status": ChargeStatus.PENDING,
        },
    )
    if not created and link.study_id != study_id:
        raise ValueError("Idempotency key is already associated with another study.")
    record_event(
        tenant_id=tenant_id,
        event_type="charge.linked",
        entity_type="ImagingStudy",
        entity_id=study_id,
        actor_id=actor_id,
        payload={"charge_id": str(charge_id), "idempotency_key": idempotency_key},
    )
    return link


def charge_links(*, tenant_id, study_id):
    return ImagingChargeLink.objects.filter(
        tenant_id=tenant_id, study_id=study_id
    ).order_by("created_at")


__all__ = ["link_charge", "charge_links"]
