from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.notes.constants import NoteType
from apps.platform.organizations.models import Organization


class ClinicalNoteTemplate(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="clinical_note_templates"
    )
    name = models.CharField(max_length=150)
    note_type = models.CharField(
        max_length=32, choices=NoteType.choices, default=NoteType.SOAP
    )
    schema = models.JSONField(default=dict, blank=True)
    default_content = models.JSONField(default=dict, blank=True)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "clinical_note_templates"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name"), name="clin_note_tpl_org_name_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("organization", "note_type", "is_active"),
                name="clin_note_tpl_lookup_idx",
            )
        ]
