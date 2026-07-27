"""
Prompt template registry for the AI platform.

Stores versioned prompt templates used by the prompt engine.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class PromptTemplate(BaseModel):
    """
    Versioned prompt template.

    Templates are referenced by name + version from the prompt engine.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="prompt_templates",
        null=True,
        blank=True,
        help_text="Owning organization. Null for global templates.",
    )

    name = models.CharField(
        max_length=120,
        help_text="Template identifier, e.g. 'clinical_note_summary'.",
    )

    version = models.CharField(
        max_length=20,
        default="1.0",
        help_text="Semantic version of the template.",
    )

    description = models.TextField(
        blank=True,
        help_text="Human readable description of the template purpose.",
    )

    template = models.TextField(
        help_text="Template body using Jinja2 syntax.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this template version is currently active.",
    )

    class Meta:
        db_table = "ai_prompt_templates"

        verbose_name = "Prompt Template"

        verbose_name_plural = "Prompt Templates"

        ordering = (
            "name",
            "-version",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "name",
                    "version",
                ],
                name="uniq_prompt_org_name_version",
            ),
        ]

    def __str__(self) -> str:
        """Return a readable label."""

        return f"{self.name} v{self.version}"


__all__ = [
    "PromptTemplate",
]
