from __future__ import annotations

import uuid

from django.db import transaction
from django.utils import timezone

from apps.imaging.models import ImagingWorkflowState, ImagingWorkflowTransition
from apps.imaging.services.audit import record_event


class WorkflowEngineError(ValueError):
    pass


@transaction.atomic
def transition(
    *,
    tenant_id,
    entity_type,
    entity_id,
    target_state,
    graph,
    actor_id=None,
    reason="",
    guard=None,
    state_model=None,
    sync=None,
):
    state = (
        ImagingWorkflowState.objects.select_for_update()
        .filter(tenant_id=tenant_id, entity_type=entity_type, entity_id=entity_id)
        .first()
    )
    if state is None:
        if state_model is None:
            raise WorkflowEngineError("Initial workflow state is required.")
        state = ImagingWorkflowState.objects.create(
            tenant_id=tenant_id,
            entity_type=entity_type,
            entity_id=entity_id,
            current_state=state_model,
            version=1,
        )
    current = getattr(state.current_state, "value", state.current_state)
    target = getattr(target_state, "value", target_state)
    current = str(current)
    target = str(target)
    if target not in graph.get(current, frozenset()):
        raise WorkflowEngineError(
            f"Illegal Imaging workflow transition: {current!r} -> {target!r}"
        )
    if guard is not None:
        guard(current, target_state)
    correlation_id = uuid.uuid4()
    state.current_state = target
    state.version += 1
    state.last_actor_id = actor_id
    state.last_transition_at = timezone.now()
    state.save(
        update_fields=[
            "current_state",
            "version",
            "last_actor_id",
            "last_transition_at",
            "updated_at",
        ]
    )
    if sync is not None:
        sync(target_state)
    ImagingWorkflowTransition.objects.create(
        tenant_id=tenant_id,
        entity_type=entity_type,
        entity_id=entity_id,
        from_state=current,
        to_state=target_state,
        transition=f"{entity_type.lower()}.{current}_to_{target}",
        actor_id=actor_id,
        correlation_id=correlation_id,
        reason=reason,
    )
    record_event(
        tenant_id=tenant_id,
        event_type="workflow.transitioned",
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        payload={
            "from_state": current,
            "to_state": target,
            "version": state.version,
            "correlation_id": str(correlation_id),
            "reason": reason,
        },
    )
    return state
