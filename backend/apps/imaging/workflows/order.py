from __future__ import annotations

from django.utils import timezone

from apps.imaging.constants.choices import ImagingOrderStatus
from apps.imaging.models import ImagingOrder
from apps.imaging.workflow_registry import ORDER_TRANSITIONS
from apps.imaging.workflows.engine import transition


def transition_order(*, order_id, tenant_id, target_state, actor_id=None, reason=""):
    order = ImagingOrder.objects.get(id=order_id, tenant_id=tenant_id)

    def sync(state):
        order.status = state
        if state == ImagingOrderStatus.CANCELLED:
            order.cancelled_at = timezone.now()
            order.cancellation_reason = reason
            order.save(
                update_fields=[
                    "status",
                    "cancelled_at",
                    "cancellation_reason",
                    "updated_at",
                ]
            )
        else:
            order.save(update_fields=["status", "updated_at"])

    return transition(
        tenant_id=tenant_id,
        entity_type="ImagingOrder",
        entity_id=order.id,
        target_state=target_state,
        graph=ORDER_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=order.status,
        sync=sync,
    )
