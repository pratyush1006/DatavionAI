from django.db import transaction

from apps.imaging.models import RadiologyReport
from apps.imaging.services.appointments import link_appointment
from apps.imaging.services.documents import link_report_document
from apps.imaging.services.revenue_cycle import link_charge
from apps.imaging.services.workflow import complete_order, finalize_report


@transaction.atomic
def complete_imaging_case(
    *,
    tenant_id,
    order_id,
    report_id,
    document_id=None,
    charge_id=None,
    procedure_code=None,
    charge_idempotency_key=None,
    appointment_id=None,
    actor_id=None,
):
    if appointment_id is not None:
        link_appointment(
            order_id=order_id,
            appointment_id=appointment_id,
            tenant_id=tenant_id,
            actor_id=actor_id,
        )
    finalize_report(report_id=report_id, tenant_id=tenant_id, radiologist_id=actor_id)
    if document_id is not None:
        link_report_document(
            report_id=report_id,
            document_id=document_id,
            tenant_id=tenant_id,
            actor_id=actor_id,
        )
    if charge_id is not None:
        if not procedure_code or not charge_idempotency_key:
            raise ValueError(
                "procedure_code and charge_idempotency_key are required with charge_id."
            )
        report = RadiologyReport.objects.get(id=report_id, tenant_id=tenant_id)
        link_charge(
            study_id=report.study_id,
            charge_id=charge_id,
            procedure_code=procedure_code,
            tenant_id=tenant_id,
            idempotency_key=charge_idempotency_key,
            actor_id=actor_id,
        )
    return complete_order(order_id=order_id, tenant_id=tenant_id, actor_id=actor_id)
