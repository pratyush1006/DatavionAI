from django.db import transaction

from apps.imaging.constants.choices import ImagingOrderStatus, ImagingStudyStatus
from apps.imaging.models import ImagingOrder, ImagingProcedure, ImagingStudy
from apps.imaging.services.audit import record_event


@transaction.atomic
def create_study(*, tenant_id, order_id, procedure_id, accession_number, actor_id=None):
    order = ImagingOrder.objects.select_for_update().get(
        id=order_id, tenant_id=tenant_id
    )
    if order.status != ImagingOrderStatus.SCHEDULED:
        raise ValueError("A study can only be created for a scheduled order.")
    procedure = ImagingProcedure.objects.get(
        id=procedure_id, tenant_id=tenant_id, active=True
    )
    study = ImagingStudy.objects.create(
        tenant_id=tenant_id,
        accession_number=accession_number,
        order=order,
        procedure=procedure,
        patient_id=order.patient_id,
        status=ImagingStudyStatus.SCHEDULED,
    )
    from apps.imaging.models import ImagingWorkflowState

    ImagingWorkflowState.objects.create(
        tenant_id=tenant_id,
        entity_type="ImagingStudy",
        entity_id=study.id,
        current_state=ImagingStudyStatus.SCHEDULED,
        version=1,
    )
    record_event(
        tenant_id=tenant_id,
        event_type="study.created",
        entity_type="ImagingStudy",
        entity_id=study.id,
        actor_id=actor_id,
        payload={"accession_number": accession_number},
    )
    return study
