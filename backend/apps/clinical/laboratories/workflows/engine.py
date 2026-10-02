from __future__ import annotations

import uuid

from django.db import transaction
from django.utils import timezone

from ..models import LaboratoryWorkflowState, LaboratoryWorkflowTransition
from ..services.audit import audit
from ..workflow_registry import assert_transition


class WorkflowEngineError(ValueError):
    pass


@transaction.atomic
def transition(
    *,
    organization_id,
    workflow,
    entity_type,
    entity_id,
    target_state,
    graph,
    actor_id=None,
    reason="",
    state_model=None,
    guard=None,
    sync=None,
):
    state = (
        LaboratoryWorkflowState.objects.select_for_update()
        .filter(
            organization_id=organization_id,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        .first()
    )

    if state is None:
        if state_model is None:
            raise WorkflowEngineError("Initial Laboratory workflow state is required.")
        state = LaboratoryWorkflowState.objects.create(
            organization_id=organization_id,
            entity_type=entity_type,
            entity_id=entity_id,
            workflow=workflow,
            current_state=str(getattr(state_model, "value", state_model)),
            version=1,
        )

    current = str(state.current_state)
    target = str(getattr(target_state, "value", target_state))

    if state.workflow != workflow:
        raise WorkflowEngineError(
            f"Workflow mismatch: state={state.workflow!r}, requested={workflow!r}"
        )

    try:
        assert_transition(graph, current, target)
    except ValueError as exc:
        raise WorkflowEngineError(str(exc)) from exc

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

    LaboratoryWorkflowTransition.objects.create(
        organization_id=organization_id,
        entity_type=entity_type,
        entity_id=entity_id,
        workflow=workflow,
        from_state=current,
        to_state=target,
        transition=f"{workflow}.{current}_to_{target}",
        actor_id=actor_id,
        correlation_id=correlation_id,
        reason=reason,
    )

    audit(
        organization_id,
        actor_id,
        "workflow.transitioned",
        entity_type,
        entity_id,
        {
            "workflow": workflow,
            "from_state": current,
            "to_state": target,
            "correlation_id": str(correlation_id),
        },
    )
    return state
