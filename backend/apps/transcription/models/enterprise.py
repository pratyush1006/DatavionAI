from __future__ import annotations

import uuid

from django.db import models


class TranscriptionIdempotencyKey(models.Model):
    key_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="transcription_idempotency_keys",
    )
    scope = models.CharField(max_length=80)
    idempotency_key = models.CharField(max_length=160)
    request_hash = models.CharField(max_length=128)
    response_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transcription_idempotency_keys"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "scope", "idempotency_key"),
                name="trans_idem_org_scope_key",
            )
        ]
        indexes = [
            models.Index(
                fields=("organization", "scope"), name="trans_idem_org_scope_idx"
            )
        ]


class TranscriptionOutboxEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="transcription_outbox_events",
    )
    event_type = models.CharField(max_length=120)
    aggregate_type = models.CharField(max_length=80)
    aggregate_id = models.CharField(max_length=160)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="pending")
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transcription_outbox_events"
        indexes = [
            models.Index(
                fields=("organization", "status"), name="trans_out_org_status_idx"
            ),
            models.Index(
                fields=("status", "available_at"), name="trans_out_status_time_idx"
            ),
        ]
