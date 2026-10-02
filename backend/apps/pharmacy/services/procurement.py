from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.pharmacy.constants import ApprovalStatus, PurchaseOrderStatus
from apps.pharmacy.models import ProcurementApproval, PurchaseOrder
from apps.pharmacy.services.audit import record_audit
from apps.pharmacy.services.events import enqueue_event


@transaction.atomic
def request_purchase_approval(*, organization, purchase_order, actor_id=None):
    purchase_order = PurchaseOrder.objects.select_for_update().get(pk=purchase_order.pk)
    if purchase_order.organization_id != organization.id:
        raise ValidationError("Purchase order is outside the organization scope.")
    if purchase_order.status != PurchaseOrderStatus.DRAFT:
        raise ValidationError(
            "Only draft purchase orders can be submitted for approval."
        )
    approval, _ = ProcurementApproval.objects.update_or_create(
        purchase_order=purchase_order,
        defaults={
            "organization": organization,
            "status": ApprovalStatus.PENDING,
            "requested_by_id": getattr(actor_id, "pk", actor_id) if actor_id else None,
            "decided_by_id": None,
            "decided_at": None,
            "reason": "",
        },
    )
    record_audit(
        organization=organization,
        action="procurement.approval_requested",
        entity_type="PurchaseOrder",
        entity_id=purchase_order.id,
        actor_id=actor_id,
    )
    return approval


@transaction.atomic
def decide_purchase_approval(
    *, organization, approval, approved, actor_id=None, reason=""
):
    locked = (
        ProcurementApproval.objects.select_for_update()
        .select_related("purchase_order")
        .get(pk=approval.pk)
    )
    if locked.organization_id != organization.id:
        raise ValidationError("Approval is outside the organization scope.")
    if locked.status != ApprovalStatus.PENDING:
        raise ValidationError("Procurement approval is already decided.")
    actor_value = getattr(actor_id, "pk", actor_id) if actor_id else None
    if approved and actor_value is not None and locked.requested_by_id == actor_value:
        raise ValidationError("The requester cannot approve the same purchase order.")
    if not approved and not str(reason).strip():
        raise ValidationError("A rejection reason is required.")
    locked.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
    locked.decided_by_id = getattr(actor_id, "pk", actor_id) if actor_id else None
    locked.decided_at = timezone.now()
    locked.reason = reason
    locked.save(
        update_fields=["status", "decided_by_id", "decided_at", "reason", "updated_at"]
    )
    if approved:
        locked.purchase_order.status = PurchaseOrderStatus.ORDERED
        locked.purchase_order.ordered_at = timezone.now()
        locked.purchase_order.save(update_fields=["status", "ordered_at", "updated_at"])
    record_audit(
        organization=organization,
        action="procurement.approval_decided",
        entity_type="PurchaseOrder",
        entity_id=locked.purchase_order_id,
        actor_id=actor_id,
        payload={"approved": approved, "reason": reason},
    )
    if approved:
        enqueue_event(
            organization=organization,
            event_type="pharmacy.purchase_approved",
            aggregate_type="PurchaseOrder",
            aggregate_id=locked.purchase_order_id,
            payload={"purchase_order_id": str(locked.purchase_order_id)},
        )
    return locked
