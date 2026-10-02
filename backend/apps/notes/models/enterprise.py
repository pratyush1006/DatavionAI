from __future__ import annotations

import uuid

from django.db import models

from apps.notes.models.note import ClinicalNote
from apps.platform.organizations.models import Organization


class NoteIdempotencyKey(models.Model):
    key_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="clinical_note_idempotency_keys",
    )
    scope = models.CharField(max_length=100)
    idempotency_key = models.CharField(max_length=160)
    request_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clinical_note_idempotency_keys"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "scope", "idempotency_key"),
                name="clin_note_idem_org_scope_key_uniq",
            )
        ]


class NoteOutboxEvent(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="clinical_note_outbox_events",
    )
    event_type = models.CharField(max_length=120)
    aggregate_type = models.CharField(max_length=80)
    aggregate_id = models.CharField(max_length=160)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="pending", db_index=True)
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clinical_note_outbox_events"
        indexes = [
            models.Index(
                fields=("organization", "status"), name="clin_note_out_org_status_idx"
            ),
            models.Index(
                fields=("status", "available_at"), name="clin_note_out_status_time_idx"
            ),
        ]


class NoteTransition(models.Model):
    transition_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="clinical_note_transitions"
    )
    note = models.ForeignKey(
        ClinicalNote, on_delete=models.PROTECT, related_name="transition_ledger"
    )
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    actor = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="clinical_note_transitions",
    )
    version = models.PositiveIntegerField()
    reason = models.TextField(blank=True)
    correlation_id = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clinical_note_transitions"
        indexes = [
            models.Index(
                fields=("organization", "note", "created_at"),
                name="clin_note_tr_org_note_idx",
            )
        ]
