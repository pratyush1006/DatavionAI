"""Read-only, RBAC-protected adapters to canonical Datavion domain modules."""

from __future__ import annotations

from apps.ai.services.rbac import AI_VIEW, require_ai_permission

LABORATORY_MODULE = "clinical.laboratories"
LABORATORY_ORDER_RESOURCE = "laboratory_order"


def get_laboratory_order_status(
    *,
    user,
    tenant,
    organization,
    order_number: str,
    module_code: str = LABORATORY_MODULE,
    resource_type: str = LABORATORY_ORDER_RESOURCE,
):
    require_ai_permission(user=user, organization=organization, permission=AI_VIEW)
    if module_code != LABORATORY_MODULE or resource_type != LABORATORY_ORDER_RESOURCE:
        raise ValueError(
            "Laboratory status lookup requires the canonical clinical.laboratories module reference."
        )
    from apps.clinical.laboratories.models import LaboratoryOrder

    order = (
        LaboratoryOrder.objects.select_related("patient", "laboratory")
        .filter(organization=organization, order_number=order_number)
        .first()
    )
    if not order:
        return None
    items = order.items.select_related("test").all()
    return {
        "order_number": order.order_number,
        "status": order.status,
        "patient_id": str(order.patient_id),
        "laboratory_id": str(order.laboratory_id),
        "ordered_at": order.ordered_at.isoformat() if order.ordered_at else None,
        "items": [{"test": item.test.name, "status": item.status} for item in items],
        "module_reference": {
            "module_code": LABORATORY_MODULE,
            "resource_type": LABORATORY_ORDER_RESOURCE,
            "resource_id": order.order_number,
        },
    }


__all__ = (
    "LABORATORY_MODULE",
    "LABORATORY_ORDER_RESOURCE",
    "get_laboratory_order_status",
)
