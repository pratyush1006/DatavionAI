from __future__ import annotations

import uuid

from django.db import models


class LaboratoryWorkflowState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField(db_index=True)
    workflow = models.CharField(max_length=64)
    current_state = models.CharField(max_length=64)
    version = models.PositiveIntegerField(default=1)
    last_actor_id = models.UUIDField(null=True, blank=True)
    last_transition_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "laboratories_workflow_states"
        constraints = [
            models.UniqueConstraint(
                fields=["organization_id", "entity_type", "entity_id"],
                name="uq_lab_workflow_state_entity",
            )
        ]
        indexes = [
            models.Index(
                fields=["organization_id", "workflow", "current_state"],
                name="ix_lab_workflow_state_cursor",
            ),
            models.Index(
                fields=["organization_id", "entity_id"],
                name="ix_lab_workflow_state_entity",
            ),
        ]


class LaboratoryWorkflowTransition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField(db_index=True)
    workflow = models.CharField(max_length=64)
    from_state = models.CharField(max_length=64)
    to_state = models.CharField(max_length=64)
    transition = models.CharField(max_length=128)
    actor_id = models.UUIDField(null=True, blank=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    reason = models.TextField(blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "laboratories_workflow_transitions"
        indexes = [
            models.Index(
                fields=["organization_id", "entity_type", "entity_id", "occurred_at"],
                name="ix_lab_wf_trans_entity",
            ),
            models.Index(
                fields=["organization_id", "correlation_id"],
                name="ix_lab_wf_trans_corr",
            ),
        ]
