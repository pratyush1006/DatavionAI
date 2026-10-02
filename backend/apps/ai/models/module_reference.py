"""Required references into canonical Datavion domain modules."""

from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models


class AIModuleReference(models.Model):
    """Authoritative source-module/resource reference required by domain AI workflows."""

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_module_references"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_module_references",
    )
    module_code = models.CharField(max_length=120)
    resource_type = models.CharField(max_length=120)
    resource_id = models.CharField(max_length=160)
    patient_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_module_references"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "module_code", "resource_type", "resource_id"),
                name="ai_module_ref_uniq",
            )
        ]
        indexes = [
            models.Index(
                fields=("tenant", "organization", "module_code"),
                name="ai_modref_scope_idx",
            )
        ]

    def clean(self):
        if (
            self.organization_id
            and self.tenant_id
            and self.organization.tenant_id != self.tenant_id
        ):
            raise ValidationError({"tenant": "Tenant must match organization tenant."})


__all__ = ("AIModuleReference",)
