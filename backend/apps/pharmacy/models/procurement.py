from django.db import models

from apps.core.models import BaseModel
from apps.pharmacy.constants import ApprovalStatus
from apps.pharmacy.models.purchase import PurchaseOrder


class ProcurementApproval(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="pharmacy_procurement_approvals",
    )
    purchase_order = models.OneToOneField(
        PurchaseOrder, on_delete=models.PROTECT, related_name="procurement_approval"
    )
    status = models.CharField(
        max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    requested_by_id = models.UUIDField(null=True, blank=True)
    decided_by_id = models.UUIDField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True)

    class Meta:
        db_table = "pharmacy_procurement_approvals"
        indexes = [models.Index(fields=("organization", "status"))]
