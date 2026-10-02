from django.db import models

from apps.clinical.appointments.models import Appointment
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.providers.models import Provider
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class Encounter(BaseModel):
    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="encounters",
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.PROTECT,
        related_name="encounters",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="encounters",
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="encounters",
    )
    encounter_number = models.CharField(max_length=50, db_index=True)
    status = models.CharField(
        max_length=30,
        choices=EncounterStatus.choices,
        default=EncounterStatus.SCHEDULED,
        db_index=True,
    )
    chief_complaint = models.TextField(blank=True)
    history_of_present_illness = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    clinical_notes = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_billable = models.BooleanField(default=True)

    class Meta:
        db_table = "encounters"
        ordering = ("-started_at", "-created_at")
        indexes = [
            models.Index(fields=("started_at",), name="encounters_started_3d026b_idx"),
            models.Index(
                fields=("provider", "started_at"), name="encounters_provide_ab015f_idx"
            ),
            models.Index(
                fields=("patient", "started_at"), name="encounters_patient_fc3997_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "encounter_number"),
                name="unique_encounter_number_per_organization",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.encounter_number} | {self.patient_id} | {self.status}"
