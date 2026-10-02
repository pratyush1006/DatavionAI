from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction
from django.utils import timezone

from .integrations import require_integration
from .models import (
    Admission,
    Bed,
    OPDQueue,
    OPDVisit,
    OperationalEvent,
    OperationalUnit,
)
from .services import (
    assign_bed,
    discharge_patient,
    register_opd_visit,
    transfer_patient,
)

WORKFLOW_STAGES = (
    "patient",
    "opd",
    "encounter",
    "admission",
    "bed",
    "ward_icu",
    "laboratory",
    "imaging",
    "pharmacy",
    "rcm",
    "discharge",
    "notifications",
    "audit",
    "ai",
)

EXTERNAL_BOUNDARIES = {
    "encounter": "encounters",
    "laboratory": "laboratory",
    "imaging": "imaging",
    "pharmacy": "pharmacy",
    "rcm": "rcm",
    "notifications": "notifications",
    "audit": "audit",
    "ai": "ai",
}


@dataclass(frozen=True)
class WorkflowResult:
    stage: str
    reference: str
    metadata: dict


def validate_workflow_boundaries() -> dict[str, str]:
    return {
        stage: require_integration(key)["resolved_app"]
        for stage, key in EXTERNAL_BOUNDARIES.items()
    }


@transaction.atomic
def register_opd_workflow(
    *, queue: OPDQueue, patient, tenant, organization, encounter_reference=""
) -> OPDVisit:
    visit = register_opd_visit(
        queue=queue,
        patient=patient,
        tenant=tenant,
        organization=organization,
        encounter_reference=encounter_reference,
    )
    _integration_event(
        tenant,
        organization,
        "encounter",
        visit,
        patient.pk,
        {"opd_visit_id": str(visit.uuid)},
    )
    return visit


@transaction.atomic
def admit_workflow(
    *,
    patient,
    unit: OperationalUnit,
    bed: Bed,
    tenant,
    organization,
    admission_number: str,
    reason="",
) -> Admission:
    admission = Admission.objects.create(
        tenant=tenant,
        organization=organization,
        patient=patient,
        unit=unit,
        admission_number=admission_number,
        admitted_at=timezone.now(),
        reason=reason,
    )
    assignment = assign_bed(
        bed=bed,
        patient=patient,
        tenant=tenant,
        organization=organization,
        admission_reference=admission.admission_number,
    )
    admission.bed_assignment = assignment
    admission.save(update_fields=("bed_assignment", "updated_at"))
    for stage in (
        "laboratory",
        "imaging",
        "pharmacy",
        "rcm",
        "notifications",
        "audit",
        "ai",
    ):
        _integration_event(
            tenant,
            organization,
            stage,
            admission,
            patient.pk,
            {"admission_id": str(admission.uuid)},
        )
    return admission


@transaction.atomic
def transfer_workflow(
    *,
    admission: Admission,
    to_unit: OperationalUnit,
    to_bed: Bed,
    tenant,
    organization,
    reason="",
    icu=False,
):
    movement = transfer_patient(
        admission=admission,
        to_unit=to_unit,
        to_bed=to_bed,
        tenant=tenant,
        organization=organization,
        reason=reason,
        icu=icu,
    )
    _integration_event(
        tenant,
        organization,
        "notifications",
        movement,
        admission.patient_id,
        {"movement_id": str(movement.uuid)},
    )
    _integration_event(
        tenant,
        organization,
        "audit",
        movement,
        admission.patient_id,
        {"movement_id": str(movement.uuid)},
    )
    return movement


@transaction.atomic
def discharge_workflow(*, admission: Admission, tenant, organization):
    admission = discharge_patient(
        admission=admission, tenant=tenant, organization=organization
    )
    for stage in ("rcm", "notifications", "audit", "ai"):
        _integration_event(
            tenant,
            organization,
            stage,
            admission,
            admission.patient_id,
            {"admission_id": str(admission.uuid)},
        )
    return admission


def _integration_event(tenant, organization, stage, entity, patient_id, metadata):
    key = EXTERNAL_BOUNDARIES.get(stage, stage)
    if key in {
        item.key
        for item in __import__(
            "apps.hospital_operations.integrations", fromlist=["INTEGRATIONS"]
        ).INTEGRATIONS
    }:
        require_integration(key)
    return OperationalEvent.objects.create(
        tenant=tenant,
        organization=organization,
        event_type=f"integration_{stage}",
        entity_type=entity.__class__.__name__,
        entity_id=entity.uuid,
        patient_id=patient_id,
        correlation_id=f"workflow-{entity.uuid}",
        metadata={"stage": stage, **metadata},
    )
