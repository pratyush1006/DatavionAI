"""Assemble a minimal patient-owned dashboard projection."""

from __future__ import annotations

from django.utils import timezone

from apps.clinical.appointments.constants import AppointmentStatus
from apps.clinical.appointments.selectors import AppointmentSelector
from apps.clinical.laboratories.selectors.reports import reports
from apps.clinical.prescriptions.constants import PrescriptionStatus
from apps.clinical.prescriptions.selectors import PrescriptionSelector
from apps.patient_management.patient_documents.constants import PatientDocumentStatus
from apps.patient_management.patient_documents.selectors import (
    patient_document_queryset,
)


def build_patient_dashboard(*, account):
    """Build counts and summaries scoped to one portal account's patient."""
    patient = account.patient
    organization = account.organization
    now = timezone.now()
    today = timezone.localdate()

    appointments = (
        AppointmentSelector.for_patient(
            organization=organization,
            patient_id=patient.pk,
        )
        .filter(
            scheduled_start__gte=now,
            status__in=(AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED),
        )
        .select_related("provider__employee")
        .order_by("scheduled_start")
    )
    prescriptions = (
        PrescriptionSelector.list(organization_id=organization.pk)
        .filter(
            patient_id=patient.pk,
            status=PrescriptionStatus.ACTIVE,
            start_date__lte=today,
            end_date__gte=today,
            is_deleted=False,
        )
        .select_related("medication")
    )
    lab_reports = (
        reports(organization.pk)
        .filter(
            order__organization_id=organization.pk,
            order__patient_id=patient.pk,
            status="released",
            released_at__isnull=False,
            is_deleted=False,
        )
        .select_related("order")
        .order_by("-released_at")
    )
    documents = (
        patient_document_queryset(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
            patient_id=patient.pk,
        )
        .filter(
            status=PatientDocumentStatus.ACTIVE,
            is_confidential=False,
        )
        .order_by("-uploaded_at", "-created_at")
    )

    next_appointment = appointments.first()
    appointment_summary = None
    if next_appointment is not None:
        appointment_summary = {
            "provider_name": next_appointment.provider.display_name,
            "scheduled_start": next_appointment.scheduled_start,
            "appointment_type": next_appointment.appointment_type,
            "status": next_appointment.status,
            "is_virtual": next_appointment.is_virtual,
        }

    updates = []
    for report in lab_reports[:5]:
        updates.append(
            {
                "id": f"lab:{report.pk}",
                "category": "lab_report",
                "title": report.title,
                "occurred_at": report.released_at,
            }
        )
    for prescription in prescriptions.order_by("-created_at")[:5]:
        updates.append(
            {
                "id": f"prescription:{prescription.pk}",
                "category": "prescription",
                "title": prescription.medication.display_name,
                "occurred_at": prescription.created_at,
            }
        )
    for document in documents[:5]:
        updates.append(
            {
                "id": f"document:{document.pk}",
                "category": "document",
                "title": document.title,
                "occurred_at": document.uploaded_at or document.created_at,
            }
        )
    updates.sort(key=lambda update: update["occurred_at"], reverse=True)

    return {
        "patient": {
            "id": str(patient.pk),
            "display_name": patient.display_name,
        },
        "counts": {
            "upcoming_appointments": appointments.count(),
            "active_prescriptions": prescriptions.count(),
            "lab_reports": lab_reports.count(),
            "documents": documents.count(),
        },
        "upcoming_appointment": appointment_summary,
        "health_updates": updates[:5],
    }


__all__ = ("build_patient_dashboard",)
