"""Department-specific AI application registry."""

from __future__ import annotations

import uuid

from django.db import models


class AIApplication(models.Model):
    """An organization-scoped AI product such as Clinical AI or Laboratory AI."""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_applications"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_applications",
    )
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(("active", "Active"), ("inactive", "Inactive")),
        default="active",
    )
    department = models.CharField(max_length=80, blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_applications"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "code"), name="ai_app_org_code_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="ai_app_tenant_org_idx"
            ),
            models.Index(
                fields=("organization", "status"), name="ai_app_org_status_idx"
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.tenant_id
            and self.organization_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})

    def __str__(self):
        return self.name
