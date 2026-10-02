from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.imaging.constants.choices import (
    AppointmentLinkStatus,
    ChargeStatus,
    ContrastStatus,
    DocumentLinkStatus,
    ImagingOrderStatus,
    ImagingReportStatus,
    ImagingStudyStatus,
    IntegrationStatus,
    ModalityType,
    Priority,
    ProcedureType,
)


class TenantStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    organization_id = models.UUIDField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImagingModality(TenantStampedModel):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=160)
    modality_type = models.CharField(max_length=32, choices=ModalityType.choices)
    facility_id = models.UUIDField(null=True, blank=True, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "imaging_modalities"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "code"],
                name="uq_imaging_modality_tenant_code",
            )
        ]
        indexes = [
            models.Index(fields=["tenant_id", "modality_type", "active"]),
        ]


class ImagingOrder(TenantStampedModel):
    order_number = models.CharField(max_length=64)
    patient_id = models.UUIDField(db_index=True)
    encounter_id = models.UUIDField(null=True, blank=True, db_index=True)
    ordering_provider_id = models.UUIDField(null=True, blank=True, db_index=True)
    clinical_indication = models.TextField()
    priority = models.CharField(
        max_length=16, choices=Priority.choices, default=Priority.ROUTINE
    )
    status = models.CharField(
        max_length=32,
        choices=ImagingOrderStatus.choices,
        default=ImagingOrderStatus.DRAFT,
    )
    authorization_reference = models.CharField(max_length=128, blank=True)
    readiness_notes = models.TextField(blank=True)
    ordered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        db_table = "imaging_orders"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "order_number"],
                name="uq_imaging_order_tenant_number",
            )
        ]
        indexes = [
            models.Index(fields=["tenant_id", "patient_id", "status"]),
            models.Index(fields=["tenant_id", "encounter_id"]),
            models.Index(fields=["tenant_id", "priority", "status"]),
        ]


class ImagingProcedure(TenantStampedModel):
    procedure_code = models.CharField(max_length=64)
    name = models.CharField(max_length=200)
    modality = models.ForeignKey(
        ImagingModality, on_delete=models.PROTECT, related_name="procedures"
    )
    procedure_type = models.CharField(
        max_length=32,
        choices=ProcedureType.choices,
        default=ProcedureType.DIAGNOSTIC,
    )
    body_region = models.CharField(max_length=160, blank=True)
    contrast_required = models.BooleanField(default=False)
    cect = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def clean(self):
        if self.cect and self.modality.modality_type != ModalityType.CT:
            raise ValidationError("CECT procedures must use a CT modality.")

    class Meta:
        db_table = "imaging_procedures"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "procedure_code"],
                name="uq_imaging_procedure_tenant_code",
            )
        ]
        indexes = [
            models.Index(fields=["tenant_id", "modality", "active"]),
        ]


class ImagingStudy(TenantStampedModel):
    accession_number = models.CharField(max_length=64)
    order = models.ForeignKey(
        ImagingOrder, on_delete=models.PROTECT, related_name="studies"
    )
    procedure = models.ForeignKey(
        ImagingProcedure, on_delete=models.PROTECT, related_name="studies"
    )
    patient_id = models.UUIDField(db_index=True)
    study_instance_uid = models.CharField(max_length=128, blank=True, db_index=True)
    status = models.CharField(
        max_length=32,
        choices=ImagingStudyStatus.choices,
        default=ImagingStudyStatus.SCHEDULED,
    )
    performed_at = models.DateTimeField(null=True, blank=True)
    acquired_by_id = models.UUIDField(null=True, blank=True)
    acquisition_notes = models.TextField(blank=True)
    external_reference = models.CharField(max_length=256, blank=True)

    class Meta:
        db_table = "imaging_studies"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "accession_number"],
                name="uq_imaging_study_tenant_accession",
            )
        ]
        indexes = [
            models.Index(fields=["tenant_id", "patient_id", "status"]),
            models.Index(fields=["tenant_id", "study_instance_uid"]),
        ]


class ContrastAssessment(TenantStampedModel):
    study = models.OneToOneField(
        ImagingStudy, on_delete=models.CASCADE, related_name="contrast_assessment"
    )
    status = models.CharField(
        max_length=32,
        choices=ContrastStatus.choices,
        default=ContrastStatus.NOT_REQUIRED,
    )
    allergy_screened = models.BooleanField(default=False)
    renal_screened = models.BooleanField(default=False)
    pregnancy_screened = models.BooleanField(default=False)
    screening_notes = models.TextField(blank=True)
    assessed_by_id = models.UUIDField(null=True, blank=True)
    assessed_at = models.DateTimeField(null=True, blank=True)
    administration_reference = models.CharField(max_length=128, blank=True)
    administered_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.status == ContrastStatus.CLEARED and not all(
            (self.allergy_screened, self.renal_screened, self.pregnancy_screened)
        ):
            raise ValidationError(
                "Contrast clearance requires configured screening checks."
            )

    class Meta:
        db_table = "imaging_contrast_assessments"


class ImagingFinding(TenantStampedModel):
    study = models.ForeignKey(
        ImagingStudy, on_delete=models.CASCADE, related_name="findings"
    )
    finding_code = models.CharField(max_length=64, blank=True)
    body = models.TextField()
    severity = models.CharField(max_length=32, default="unspecified")
    body_site = models.CharField(max_length=160, blank=True)
    created_by_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = "imaging_findings"
        indexes = [
            models.Index(fields=["tenant_id", "study", "created_at"]),
        ]


class RadiologyReport(TenantStampedModel):
    study = models.OneToOneField(
        ImagingStudy, on_delete=models.PROTECT, related_name="report"
    )
    status = models.CharField(
        max_length=32,
        choices=ImagingReportStatus.choices,
        default=ImagingReportStatus.DRAFT,
    )
    indication = models.TextField(blank=True)
    technique = models.TextField(blank=True)
    findings_text = models.TextField(blank=True)
    impression = models.TextField(blank=True)
    radiologist_id = models.UUIDField(null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    def clean(self):
        if (
            self.status in {ImagingReportStatus.FINAL, ImagingReportStatus.AMENDED}
            and not self.impression.strip()
        ):
            raise ValidationError("Final or amended reports require an impression.")

    class Meta:
        db_table = "imaging_radiology_reports"
        indexes = [
            models.Index(fields=["tenant_id", "status", "signed_at"]),
        ]


class RadiologyReportVersion(TenantStampedModel):
    report = models.ForeignKey(
        RadiologyReport, on_delete=models.PROTECT, related_name="versions"
    )
    version = models.PositiveIntegerField()
    status = models.CharField(max_length=32, choices=ImagingReportStatus.choices)
    findings_text = models.TextField(blank=True)
    impression = models.TextField(blank=True)
    authored_by_id = models.UUIDField(null=True, blank=True)
    created_reason = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "imaging_radiology_report_versions"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "report", "version"],
                name="uq_imaging_report_version",
            )
        ]


class ImagingAppointmentLink(TenantStampedModel):
    order = models.ForeignKey(
        ImagingOrder, on_delete=models.PROTECT, related_name="appointment_links"
    )
    appointment_id = models.UUIDField(db_index=True)
    status = models.CharField(
        max_length=32,
        choices=AppointmentLinkStatus.choices,
        default=AppointmentLinkStatus.RESERVED,
    )
    linked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "imaging_appointment_links"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "appointment_id"],
                name="uq_imaging_appointment_link",
            )
        ]


class ImagingDocumentLink(TenantStampedModel):
    report = models.ForeignKey(
        RadiologyReport, on_delete=models.PROTECT, related_name="document_links"
    )
    document_id = models.UUIDField(db_index=True)
    status = models.CharField(
        max_length=32,
        choices=DocumentLinkStatus.choices,
        default=DocumentLinkStatus.PENDING,
    )
    linked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "imaging_document_links"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "document_id"],
                name="uq_imaging_document_link",
            )
        ]


class ImagingChargeLink(TenantStampedModel):
    study = models.ForeignKey(
        ImagingStudy, on_delete=models.PROTECT, related_name="charge_links"
    )
    charge_id = models.UUIDField(db_index=True)
    procedure_code = models.CharField(max_length=64)
    status = models.CharField(
        max_length=32,
        choices=ChargeStatus.choices,
        default=ChargeStatus.PENDING,
    )
    idempotency_key = models.CharField(max_length=128)

    class Meta:
        db_table = "imaging_charge_links"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "idempotency_key"],
                name="uq_imaging_charge_idempotency",
            )
        ]


class ImagingStudyReference(TenantStampedModel):
    study = models.OneToOneField(
        ImagingStudy, on_delete=models.PROTECT, related_name="reference"
    )
    pacs_system = models.CharField(max_length=128, blank=True)
    study_instance_uid = models.CharField(max_length=128, blank=True)
    series_count = models.PositiveIntegerField(null=True, blank=True)
    storage_object_key = models.CharField(max_length=512, blank=True)
    checksum = models.CharField(max_length=128, blank=True)
    integration_status = models.CharField(
        max_length=32,
        choices=IntegrationStatus.choices,
        default=IntegrationStatus.PENDING,
    )

    class Meta:
        db_table = "imaging_study_references"


class ImagingAuditEvent(TenantStampedModel):
    event_type = models.CharField(max_length=128)
    entity_type = models.CharField(max_length=128)
    entity_id = models.UUIDField()
    actor_id = models.UUIDField(null=True, blank=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    payload = models.JSONField(default=dict)

    class Meta:
        db_table = "imaging_audit_events"
        indexes = [
            models.Index(fields=["tenant_id", "entity_type", "entity_id"]),
            models.Index(fields=["tenant_id", "event_type", "created_at"]),
        ]
