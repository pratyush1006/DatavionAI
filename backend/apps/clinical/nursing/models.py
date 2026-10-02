from __future__ import annotations

from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel


class PatientAssignment(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nursing_assignments",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="nursing_assignments",
    )
    nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        related_name="nursing_assignments",
    )
    ward = models.ForeignKey(
        "hospital_operations.OperationalUnit",
        on_delete=models.PROTECT,
        related_name="nursing_assignments",
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(("active", "Active"), ("ended", "Ended")),
        default="active",
        db_index=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "nursing_patient_assignments"
        ordering = ("-started_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("patient",),
                condition=Q(status="active"),
                name="nursing_one_active_patient_assignment",
            )
        ]


class NursingTask(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nursing_tasks",
    )
    patient = models.ForeignKey(
        "patient_core.Patient", on_delete=models.PROTECT, related_name="nursing_tasks"
    )
    assigned_nurse = models.ForeignKey(
        "providers.Provider", on_delete=models.PROTECT, related_name="nursing_tasks"
    )
    assignment = models.ForeignKey(
        PatientAssignment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    task_type = models.CharField(
        max_length=30,
        choices=(
            ("medication", "Medication"),
            ("vitals", "Vitals"),
            ("care", "Care"),
            ("review", "Review"),
            ("other", "Other"),
        ),
        default="care",
    )
    priority = models.CharField(
        max_length=20,
        choices=(
            ("routine", "Routine"),
            ("urgent", "Urgent"),
            ("critical", "Critical"),
        ),
        default="routine",
    )
    due_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("in_progress", "In progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ),
        default="pending",
        db_index=True,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_nursing_tasks",
    )
    completion_notes = models.TextField(blank=True)

    class Meta:
        db_table = "nursing_tasks"
        ordering = ("due_at",)


class MedicationAdministration(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="medication_administrations",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="medication_administrations",
    )
    prescription = models.ForeignKey(
        "prescriptions.Prescription",
        on_delete=models.PROTECT,
        related_name="administrations",
    )
    nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        related_name="medication_administrations",
    )
    scheduled_at = models.DateTimeField()
    administered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ("scheduled", "Scheduled"),
            ("administered", "Administered"),
            ("held", "Held"),
            ("refused", "Refused"),
            ("missed", "Missed"),
        ),
        default="scheduled",
        db_index=True,
    )
    dose = models.CharField(max_length=80)
    route = models.CharField(max_length=80, blank=True)
    site = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "nursing_medication_administrations"
        ordering = ("scheduled_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("prescription", "scheduled_at"),
                name="nursing_unique_scheduled_dose",
            )
        ]


class CarePlan(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nursing_care_plans",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.PROTECT,
        related_name="nursing_care_plans",
    )
    primary_nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        related_name="primary_care_plans",
    )
    title = models.CharField(max_length=180)
    diagnosis = models.TextField(blank=True)
    goals = models.JSONField(default=list)
    interventions = models.JSONField(default=list)
    evaluation = models.TextField(blank=True)
    review_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ("draft", "Draft"),
            ("active", "Active"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ),
        default="draft",
        db_index=True,
    )
    version = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "nursing_care_plans"
        ordering = ("-updated_at",)


class ClinicalAlert(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nursing_alerts",
    )
    patient = models.ForeignKey(
        "patient_core.Patient", on_delete=models.PROTECT, related_name="nursing_alerts"
    )
    assigned_nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assigned_clinical_alerts",
    )
    source_type = models.CharField(max_length=40, default="manual")
    source_reference = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=180)
    message = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=(("info", "Info"), ("warning", "Warning"), ("critical", "Critical")),
        default="warning",
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ("open", "Open"),
            ("acknowledged", "Acknowledged"),
            ("escalated", "Escalated"),
            ("resolved", "Resolved"),
        ),
        default="open",
        db_index=True,
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="acknowledged_clinical_alerts",
    )
    escalated_at = models.DateTimeField(null=True, blank=True)
    escalated_to = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="escalated_clinical_alerts",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        db_table = "nursing_clinical_alerts"
        ordering = ("-created_at",)


class NurseSchedule(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nurse_schedules",
    )
    nurse = models.ForeignKey(
        "providers.Provider", on_delete=models.PROTECT, related_name="nurse_schedules"
    )
    ward = models.ForeignKey(
        "hospital_operations.OperationalUnit",
        on_delete=models.PROTECT,
        related_name="nurse_schedules",
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    shift_type = models.CharField(
        max_length=20,
        choices=(
            ("morning", "Morning"),
            ("evening", "Evening"),
            ("night", "Night"),
            ("custom", "Custom"),
        ),
        default="custom",
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ("scheduled", "Scheduled"),
            ("active", "Active"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ),
        default="scheduled",
        db_index=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "nursing_schedules"
        ordering = ("starts_at",)


class ShiftHandover(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="nursing_handovers",
    )
    schedule = models.ForeignKey(
        NurseSchedule, on_delete=models.PROTECT, related_name="handovers"
    )
    from_nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        related_name="outgoing_handovers",
    )
    to_nurse = models.ForeignKey(
        "providers.Provider",
        on_delete=models.PROTECT,
        related_name="incoming_handovers",
    )
    ward = models.ForeignKey(
        "hospital_operations.OperationalUnit",
        on_delete=models.PROTECT,
        related_name="nursing_handovers",
    )
    patients = models.ManyToManyField(
        "patient_core.Patient", related_name="nursing_handovers"
    )
    summary = models.TextField()
    outstanding_tasks = models.JSONField(default=list)
    safety_concerns = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("accepted", "Accepted"),
        ),
        default="draft",
        db_index=True,
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "nursing_shift_handovers"
        ordering = ("-created_at",)
