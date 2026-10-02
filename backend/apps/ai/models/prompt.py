"""Reusable organization-scoped AI prompt templates."""

from __future__ import annotations

import uuid

from django.db import models


class PromptTemplate(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="ai_prompt_templates",
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_prompt_templates",
    )
    application = models.ForeignKey(
        "ai.AIApplication",
        on_delete=models.CASCADE,
        related_name="prompt_templates",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=100, null=True, blank=True)
    template = models.TextField()
    variables = models.JSONField(default=list, blank=True)
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_prompt_templates"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "application", "code", "version"),
                name="ai_prompt_version_uniq",
            )
        ]
