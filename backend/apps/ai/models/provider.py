"""AI provider and model configuration."""

from __future__ import annotations

import uuid

from django.db import models


class AIProvider(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_providers"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_providers",
    )
    name = models.CharField(max_length=120)
    provider_type = models.CharField(max_length=30)
    endpoint = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_providers"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name"), name="ai_provider_org_name_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="ai_prov_tenant_org_idx"
            ),
            models.Index(
                fields=("organization", "is_active"), name="ai_prov_org_active_idx"
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.organization_id
            and self.tenant_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})


class AIModel(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    provider = models.ForeignKey(
        AIProvider,
        on_delete=models.CASCADE,
        related_name="models",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=160)
    model_identifier = models.CharField(max_length=160, null=True, blank=True)
    capabilities = models.JSONField(default=list, blank=True)
    context_window = models.PositiveIntegerField(default=128000)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_models"
        constraints = [
            models.UniqueConstraint(
                fields=("provider", "model_identifier"),
                name="ai_model_provider_id_uniq",
            )
        ]
