"""Organization AI configuration."""

from __future__ import annotations

import uuid

from django.db import models


class AIConfiguration(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_configurations"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_configurations",
    )
    application = models.ForeignKey(
        "ai.AIApplication", on_delete=models.CASCADE, related_name="configurations"
    )
    provider = models.ForeignKey(
        "ai.AIProvider", on_delete=models.PROTECT, related_name="configurations"
    )
    model = models.ForeignKey(
        "ai.AIModel", on_delete=models.PROTECT, related_name="configurations"
    )
    temperature = models.DecimalField(max_digits=4, decimal_places=3, default=0)
    max_tokens = models.PositiveIntegerField(default=2048)
    system_prompt = models.TextField(blank=True)
    retrieval_enabled = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_configurations"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "application"), name="ai_config_org_app_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="ai_cfg_tenant_org_idx"
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.organization_id
            and self.tenant_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})
        if (
            self.application_id
            and self.organization_id
            and self.application.organization_id != self.organization_id
        ):
            raise ValidationError(
                {"application": "AI application must belong to organization."}
            )
        if (
            self.provider_id
            and self.organization_id
            and self.provider.organization_id != self.organization_id
        ):
            raise ValidationError(
                {"provider": "AI provider must belong to organization."}
            )
