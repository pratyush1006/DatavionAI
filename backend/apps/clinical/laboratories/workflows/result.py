from ..models import LaboratoryResult
from ..workflow_registry import RESULT_TRANSITIONS
from .engine import transition


def transition_result(
    *, result_id, organization_id, target_state, actor_id=None, reason=""
):
    result = LaboratoryResult.objects.select_related("order_item").get(
        id=result_id,
        organization_id=organization_id,
        is_deleted=False,
    )

    def guard(current, target):
        target_value = str(getattr(target, "value", target))
        if target_value in {"final", "corrected"}:
            if result.value_numeric is None and not result.value_text.strip():
                raise ValueError(
                    "Laboratory result requires a numeric or text value before finalization."
                )

    def sync(state):
        result.status = state
        result.save(update_fields=["status", "updated_at"])

    return transition(
        organization_id=organization_id,
        workflow="result",
        entity_type="LaboratoryResult",
        entity_id=result.id,
        target_state=target_state,
        graph=RESULT_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=result.status,
        guard=guard,
        sync=sync,
    )
