from __future__ import annotations

from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.core.models.base import BaseModel


class Medication(BaseModel):
    """Canonical clinical medication master.

    This is the single Medication entity consumed by prescriptions, pharmacy,
    and other clinical domains. Inventory/batch concepts do not belong here.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="medications",
    )
    medication_code = models.CharField(max_length=64)
    generic_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, blank=True, default="")
    strength = models.CharField(max_length=100)
    strength_unit = models.CharField(max_length=50)
    dosage_form = models.CharField(
        max_length=32,
        choices=MedicationDosageForm.choices,
    )
    route = models.CharField(
        max_length=32,
        choices=MedicationRoute.choices,
    )
    manufacturer = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    is_controlled = models.BooleanField(default=False)

    class Meta:
        db_table = "medications"
        ordering = ("generic_name", "brand_name", "strength")
        indexes = [
            models.Index(
                fields=("organization", "is_active"), name="med_org_active_idx"
            ),
            models.Index(
                fields=("organization", "generic_name"), name="med_org_generic_idx"
            ),
            models.Index(
                fields=("organization", "dosage_form", "route"),
                name="med_org_form_route_idx",
            ),
            models.Index(
                fields=("organization", "is_controlled"), name="med_org_controlled_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "medication_code"),
                name="unique_medication_code_per_organization",
            ),
        ]

    def clean(self):
        super().clean()
        for field_name in (
            "medication_code",
            "generic_name",
            "strength",
            "strength_unit",
        ):
            value = getattr(self, field_name, "")
            if not str(value).strip():
                raise ValidationError({field_name: "This field cannot be blank."})
        if self.is_deleted and self.is_active:
            raise ValidationError(
                {"is_active": "A deleted medication cannot be active."}
            )

    def save(self, *args, **kwargs):
        for field_name in (
            "medication_code",
            "generic_name",
            "brand_name",
            "strength",
            "strength_unit",
            "manufacturer",
        ):
            value = getattr(self, field_name, "")
            if isinstance(value, str):
                setattr(self, field_name, value.strip())
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def display_name(self) -> str:
        name = self.brand_name or self.generic_name
        return f"{name} {self.strength} {self.strength_unit}".strip()

    def soft_delete(self, user_id=None):
        if self.is_deleted:
            return self
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user_id is not None:
            self.deleted_by_id = user_id
        self.save(
            update_fields=[
                "is_active",
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
                "updated_at",
            ]
        )
        return self

    def restore(self):
        if not self.is_deleted:
            return self
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_id = None
        self.is_active = True
        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
                "is_active",
                "updated_at",
            ]
        )
        return self


class MedicationAuditLog(models.Model):
    """Immutable medication-master audit record."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="medication_audit_logs",
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT,
        related_name="audit_logs",
    )
    actor_id = models.UUIDField(null=True, blank=True)
    action = models.CharField(max_length=64)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medication_audit_logs"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("organization", "created_at"), name="med_audit_org_dt_idx"
            ),
            models.Index(
                fields=("medication", "created_at"), name="med_audit_med_dt_idx"
            ),
            models.Index(
                fields=("organization", "action"), name="med_audit_org_action_idx"
            ),
        ]

    def save(self, *args, **kwargs):
        if self.pk is not None and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Medication audit records are immutable.")
        return super().save(*args, **kwargs)


class MedicationOutboxEvent(models.Model):
    """Transactional outbox for medication-domain integration events."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="medication_outbox_events",
    )
    event_id = models.UUIDField(unique=True)
    event_type = models.CharField(max_length=128)
    aggregate_type = models.CharField(max_length=128)
    aggregate_id = models.UUIDField(null=True, blank=True)
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(default=timezone.now)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "medication_outbox_events"
        ordering = ("available_at", "created_at")
        indexes = [
            models.Index(
                fields=("organization", "status", "available_at"),
                name="med_out_org_stat_av_idx",
            ),
            models.Index(fields=("status", "available_at"), name="med_out_stat_av_idx"),
            models.Index(
                fields=("aggregate_type", "aggregate_id"), name="med_out_agg_idx"
            ),
        ]
