from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class ClinicalNoteVersion(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="clinical_note_versions"
    )
    note = models.ForeignKey(
        "notes.ClinicalNote", on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    structured_content = models.JSONField(default=dict, blank=True)
    changed_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="clinical_note_versions"
    )
    change_reason = models.TextField(blank=True)
    is_signed_snapshot = models.BooleanField(default=False)

    class Meta:
        db_table = "clinical_note_versions"
        constraints = [
            models.UniqueConstraint(
                fields=("note", "version_number"), name="clin_note_ver_note_num_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("organization", "note"), name="clin_note_ver_org_note_idx"
            )
        ]
