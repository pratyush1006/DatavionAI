"""Versioned clinical AI artifacts requiring clinician verification and signature."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AIClinicalArtifact(models.Model):
    NOTE_CLEANING = "note_cleaning"
    PRESCRIPTION_DRAFT = "prescription_draft"
    CLINICAL_SUMMARY = "clinical_summary"
    ARTIFACT_TYPES = (
        (NOTE_CLEANING, "Clinical Note Cleaning"),
        (PRESCRIPTION_DRAFT, "Prescription Draft"),
        (CLINICAL_SUMMARY, "Clinical Summary"),
    )
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    SIGNED = "signed"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"
    STATUSES = (
        (DRAFT, "Draft"),
        (PENDING_REVIEW, "Pending Review"),
        (VERIFIED, "Verified"),
        (SIGNED, "Signed"),
        (REJECTED, "Rejected"),
        (SUPERSEDED, "Superseded"),
    )

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_clinical_artifacts"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_clinical_artifacts",
    )
    application = models.ForeignKey(
        "ai.AIApplication", on_delete=models.PROTECT, related_name="clinical_artifacts"
    )
    module_reference = models.ForeignKey(
        "ai.AIModuleReference",
        on_delete=models.PROTECT,
        related_name="clinical_artifacts",
    )
    artifact_type = models.CharField(max_length=40, choices=ARTIFACT_TYPES)
    status = models.CharField(max_length=30, choices=STATUSES, default=DRAFT)
    current_version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ai_clinical_artifacts_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_clinical_artifacts"
        indexes = [
            models.Index(
                fields=("organization", "artifact_type", "status"),
                name="ai_artifact_scope_idx",
            ),
            models.Index(
                fields=("tenant", "organization"), name="ai_artifact_tenant_org_idx"
            ),
        ]

    def clean(self):
        if (
            self.organization_id
            and self.tenant_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})
        if (
            self.module_reference_id
            and self.module_reference.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "module_reference": "Module reference must belong to the same organization."
                }
            )


class AIClinicalArtifactVersion(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    artifact = models.ForeignKey(
        AIClinicalArtifact, on_delete=models.PROTECT, related_name="versions"
    )
    version_number = models.PositiveIntegerField()
    source_content = models.TextField(blank=True)
    normalized_content = models.TextField(blank=True)
    structured_content = models.JSONField(default=dict, blank=True)
    ai_metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ai_artifact_versions_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_clinical_artifact_versions"
        constraints = [
            models.UniqueConstraint(
                fields=("artifact", "version_number"), name="ai_artifact_version_uniq"
            )
        ]
        ordering = ("artifact", "-version_number")


class AIDoctorReview(models.Model):
    VERIFY = "verify"
    SIGN = "sign"
    REJECT = "reject"
    ACTIONS = ((VERIFY, "Verify"), (SIGN, "Sign"), (REJECT, "Reject"))
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    artifact_version = models.ForeignKey(
        AIClinicalArtifactVersion,
        on_delete=models.PROTECT,
        related_name="doctor_reviews",
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ai_doctor_reviews",
    )
    action = models.CharField(max_length=20, choices=ACTIONS)
    comments = models.TextField(blank=True)
    signature_reference = models.CharField(max_length=160, blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_doctor_reviews"
        ordering = ("-reviewed_at",)


__all__ = ("AIClinicalArtifact", "AIClinicalArtifactVersion", "AIDoctorReview")
