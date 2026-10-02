from ..models import LaboratoryOrder
from ..workflow_registry import ORDER_TRANSITIONS
from .engine import transition


def transition_order(
    *, order_id, organization_id, target_state, actor_id=None, reason=""
):
    order = LaboratoryOrder.objects.get(
        id=order_id,
        organization_id=organization_id,
        is_deleted=False,
    )

    def sync(state):
        order.status = state
        order.save(update_fields=["status", "updated_at"])

    return transition(
        organization_id=organization_id,
        workflow="order",
        entity_type="LaboratoryOrder",
        entity_id=order.id,
        target_state=target_state,
        graph=ORDER_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=order.status,
        sync=sync,
    )
