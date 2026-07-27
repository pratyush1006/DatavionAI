"""
NoteTemplate model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.notes.constants import TemplateType
from apps.platform.organizations.models import Organization


class NoteTemplate(BaseModel):
    """
    Represents a reusable clinical note template.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="note_templates",
        help_text="Organization that owns the template.",
    )

    name = models.CharField(
        max_length=255,
        help_text="Template name.",
    )

    template_type = models.CharField(
        max_length=50,
        choices=TemplateType.choices,
        help_text="Type of note template.",
    )

    content = models.JSONField(
        blank=True,
        default=dict,
        help_text="Template structure with placeholders.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether the template is currently active.",
    )

    is_system_template = models.BooleanField(
        default=False,
        help_text="Whether this is a system-provided template.",
    )

    class Meta:
        db_table = "note_templates"

        verbose_name = "Note Template"

        verbose_name_plural = "Note Templates"

        ordering = ("name",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "template_type",
                ],
                name="template_org_type_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="template_org_active_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the template display name.
        """

        return f"{self.name} ({self.get_template_type_display()})"


__all__ = [
    "NoteTemplate",
]
