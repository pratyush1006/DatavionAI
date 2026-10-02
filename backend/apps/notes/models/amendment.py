from __future__ import annotations

import uuid

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.notes.constants import AmendmentStatus
from apps.platform.organizations.models import Organization


class ClinicalNoteAmendment(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="clinical_note_amendments"
    )
    note = models.ForeignKey(
        "notes.ClinicalNote", on_delete=models.CASCADE, related_name="amendments"
    )
    amendment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    requested_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="requested_note_amendments",
    )
    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reviewed_note_amendments",
    )
    status = models.CharField(
        max_length=20,
        choices=AmendmentStatus.choices,
        default=AmendmentStatus.DRAFT,
        db_index=True,
    )
    reason = models.TextField()
    proposed_body = models.TextField()
    proposed_structured_content = models.JSONField(default=dict, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "clinical_note_amendments"
        indexes = [
            models.Index(
                fields=("organization", "status"), name="clin_note_am_org_status_idx"
            )
        ]
