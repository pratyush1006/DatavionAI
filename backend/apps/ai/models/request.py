"""AI request and usage audit records."""

from __future__ import annotations

import uuid

from django.db import models


class AIRequest(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_requests"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_requests",
    )
    application = models.ForeignKey(
        "ai.AIApplication", on_delete=models.PROTECT, related_name="requests"
    )
    module_reference = models.ForeignKey(
        "ai.AIModuleReference",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ai_requests",
    )
    conversation = models.ForeignKey(
        "ai.AIConversation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
    )
    provider = models.CharField(max_length=80)
    model = models.CharField(max_length=160)
    status = models.CharField(max_length=30, default="pending")
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    latency_ms = models.PositiveIntegerField(default=0)
    request_metadata = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "ai_requests"
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="ai_req_tenant_org_idx"
            ),
            models.Index(
                fields=("organization", "created_at"), name="ai_req_org_created_idx"
            ),
        ]


class AIUsageRecord(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    request = models.OneToOneField(
        AIRequest, on_delete=models.CASCADE, related_name="usage"
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_usage_records"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_usage_records",
    )
    provider = models.CharField(max_length=80)
    model = models.CharField(max_length=160)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    total_tokens = models.PositiveIntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_usage_records"
        indexes = [
            models.Index(
                fields=("tenant", "organization", "created_at"),
                name="ai_usage_scope_time_idx",
            )
        ]
