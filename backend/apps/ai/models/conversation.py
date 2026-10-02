"""AI conversation and message persistence."""

from __future__ import annotations

import uuid

from django.db import models


class AIConversation(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    tenant = models.ForeignKey(
        "tenancy.Tenant", on_delete=models.PROTECT, related_name="ai_conversations"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="ai_conversations",
    )
    application = models.ForeignKey(
        "ai.AIApplication", on_delete=models.PROTECT, related_name="conversations"
    )
    title = models.CharField(max_length=255, blank=True)
    user_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_conversations"
        indexes = [
            models.Index(
                fields=("tenant", "organization"), name="ai_conv_tenant_org_idx"
            ),
            models.Index(
                fields=("organization", "application"), name="ai_conv_org_app_idx"
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
        if (
            self.application_id
            and self.organization_id
            and self.application.organization_id != self.organization_id
        ):
            raise ValidationError(
                {"application": "AI application must belong to organization."}
            )


class AIMessage(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    conversation = models.ForeignKey(
        AIConversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=20)
    content = models.TextField()
    sequence = models.PositiveIntegerField(default=0)
    model = models.CharField(max_length=160, blank=True)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_messages"
        ordering = ("sequence", "created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("conversation", "sequence"), name="ai_msg_conv_seq_uniq"
            )
        ]
