from __future__ import annotations

import uuid

from django.db import models


class ImagingWorkflowState(models.Model):
    """Authoritative persisted workflow cursor for an Imaging entity."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField(db_index=True)
    current_state = models.CharField(max_length=64)
    version = models.PositiveIntegerField(default=1)
    last_actor_id = models.UUIDField(null=True, blank=True)
    last_transition_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "imaging_workflow_states"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "entity_type", "entity_id"],
                name="uq_imaging_workflow_state_entity",
            )
        ]
        indexes = [
            models.Index(fields=["tenant_id", "entity_type", "current_state"]),
            models.Index(fields=["tenant_id", "entity_id"]),
        ]


class ImagingWorkflowTransition(models.Model):
    """Immutable transition ledger for workflow audit/replay."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField(db_index=True)
    from_state = models.CharField(max_length=64)
    to_state = models.CharField(max_length=64)
    transition = models.CharField(max_length=128)
    actor_id = models.UUIDField(null=True, blank=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    reason = models.TextField(blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "imaging_workflow_transitions"
        indexes = [
            models.Index(
                fields=["tenant_id", "entity_type", "entity_id", "occurred_at"]
            ),
            models.Index(fields=["tenant_id", "transition", "occurred_at"]),
        ]
