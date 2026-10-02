from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.pharmacy.constants import BillingStatus
from apps.pharmacy.models import PharmacyBillingRecord
from apps.pharmacy.services.events import enqueue_event


@transaction.atomic
def create_dispensing_bill(*, organization, dispensing_order, actor_id=None):
    DispensingOrder = __import__("django.apps", fromlist=["apps"]).apps.get_model(
        "pharmacy", "DispensingOrder"
    )
    dispensing_order = DispensingOrder.objects.select_for_update().get(
        pk=dispensing_order.pk
    )
    if dispensing_order.organization_id != organization.id:
        raise ValidationError("Dispensing order is outside the organization scope.")
    subtotal = Decimal("0")
    tax = Decimal("0")
    for line in dispensing_order.lines.select_related("product").all():
        amount = Decimal(str(line.quantity_dispensed)) * Decimal(
            str(line.product.selling_price)
        )
        subtotal += amount
        tax += amount * Decimal(str(line.product.tax_rate)) / Decimal("100")
    record, created = PharmacyBillingRecord.objects.get_or_create(
        dispensing_order=dispensing_order,
        defaults={
            "organization": organization,
            "subtotal": subtotal,
            "tax_amount": tax,
            "total_amount": subtotal + tax,
            "status": BillingStatus.INVOICED,
        },
    )
    if created:
        enqueue_event(
            organization=organization,
            event_type="pharmacy.dispensing_billed",
            aggregate_type="PharmacyBillingRecord",
            aggregate_id=record.id,
            payload={
                "dispensing_order_id": str(dispensing_order.id),
                "total_amount": str(record.total_amount),
                "billing_record_id": str(record.id),
            },
        )
    return record, created
