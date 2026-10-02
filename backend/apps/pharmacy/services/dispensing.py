from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.pharmacy.models import DispensingLine, DispensingOrder
from apps.pharmacy.services.audit import record_audit
from apps.pharmacy.services.compliance import validate_controlled_dispensing
from apps.pharmacy.services.inventory import dispense_product

_ALLOWED_PRESCRIPTION_STATUS = {"active"}


def _validate_prescription_for_dispensing(*, organization, prescription):
    """Validate the existing DatavionOS Prescription contract before dispensing."""
    if prescription.organization_id != organization.id:
        raise ValidationError("Prescription does not belong to the organization.")
    if getattr(prescription, "is_deleted", False):
        raise ValidationError("Deleted prescriptions cannot be dispensed.")
    if hasattr(prescription, "is_active") and not prescription.is_active:
        raise ValidationError("Inactive prescriptions cannot be dispensed.")
    status = str(getattr(prescription, "status", "")).lower()
    if status not in _ALLOWED_PRESCRIPTION_STATUS:
        raise ValidationError("Only active prescriptions can be dispensed.")
    today = timezone.localdate()
    start_date = getattr(prescription, "start_date", None)
    end_date = getattr(prescription, "end_date", None)
    if start_date and today < start_date:
        raise ValidationError("Prescription is not yet effective.")
    if end_date and today > end_date:
        raise ValidationError("Prescription has expired.")
    quantity = Decimal(str(getattr(prescription, "quantity", 0)))
    refills = int(getattr(prescription, "refills", 0) or 0)
    if quantity <= 0:
        raise ValidationError("Prescription quantity must be greater than zero.")
    if refills < 0:
        raise ValidationError("Prescription refills cannot be negative.")
    return quantity, refills


def _prescription_consumed_quantity(*, prescription):
    value = (
        DispensingLine.objects.filter(
            dispensing_order__prescription=prescription,
            dispensing_order__status__in=("dispensed", "partial"),
        )
        .aggregate(total=Sum("quantity_dispensed"))
        .get("total")
    )
    return Decimal(str(value or 0))


def _validate_product_matches_prescription(*, product, prescription):
    if product.medication_id != prescription.medication_id:
        raise ValidationError(
            "Dispensing product medication does not match the prescription."
        )


@transaction.atomic
def create_dispensing_order(
    *, organization, pharmacy, prescription, dispense_number, lines, pharmacist_id=None
):
    if pharmacy.organization_id != organization.id:
        raise ValueError("Pharmacy does not belong to the organization.")
    Prescription = __import__("django.apps", fromlist=["apps"]).apps.get_model(
        "prescriptions", "Prescription"
    )
    prescription = Prescription.objects.select_for_update().get(pk=prescription.pk)
    _validate_prescription_for_dispensing(
        organization=organization, prescription=prescription
    )
    if not lines:
        raise ValidationError("At least one dispensing line is required.")

    order = DispensingOrder.objects.create(
        organization=organization,
        pharmacy=pharmacy,
        prescription=prescription,
        dispense_number=dispense_number,
        pharmacist_id=pharmacist_id,
    )
    requested_total = Decimal("0")
    for item in lines:
        product = item["product"]
        batch = item["batch"]
        quantity = Decimal(
            str(item.get("quantity_prescribed", item.get("quantity", 0)))
        )
        if (
            product.organization_id != organization.id
            or product.pharmacy_id != pharmacy.id
        ):
            raise ValueError("Dispensing product is outside the pharmacy scope.")
        if batch.product_id != product.id:
            raise ValueError("Batch does not belong to the selected product.")
        _validate_product_matches_prescription(
            product=product, prescription=prescription
        )
        if quantity <= 0:
            raise ValidationError("Dispensing quantity must be greater than zero.")
        requested_total += quantity
        payload = dict(item)
        payload.pop("quantity", None)
        payload["quantity_prescribed"] = quantity
        payload.setdefault("quantity_dispensed", Decimal("0"))
        DispensingLine.objects.create(dispensing_order=order, **payload)

    prescribed_quantity, refills = _validate_prescription_for_dispensing(
        organization=organization, prescription=prescription
    )
    maximum = prescribed_quantity * Decimal(refills + 1)
    consumed = _prescription_consumed_quantity(prescription=prescription)
    if consumed + requested_total > maximum:
        raise ValidationError(
            f"Dispensing exceeds prescription allowance. Remaining quantity: {maximum - consumed}."
        )
    return order


@transaction.atomic
def dispense_order(*, organization, order, requested_lines, pharmacist_id=None):
    """Complete dispensing atomically against the active prescription allowance."""
    if order.organization_id != organization.id:
        raise ValueError("Dispensing order is outside the organization scope.")
    if order.status in ("cancelled", "dispensed"):
        raise ValueError("Dispensing order cannot be completed in its current state.")
    if pharmacist_id is None and order.pharmacist_id is None:
        raise ValidationError("A pharmacist actor is required to complete dispensing.")
    if pharmacist_id is not None:
        order.pharmacist_id = pharmacist_id

    Prescription = __import__("django.apps", fromlist=["apps"]).apps.get_model(
        "prescriptions", "Prescription"
    )
    prescription = Prescription.objects.select_for_update().get(
        pk=order.prescription_id
    )
    prescribed_quantity, refills = _validate_prescription_for_dispensing(
        organization=organization, prescription=prescription
    )
    maximum = prescribed_quantity * Decimal(refills + 1)
    consumed = _prescription_consumed_quantity(prescription=prescription)

    if not requested_lines:
        raise ValidationError("At least one dispensing request is required.")

    requested_total = Decimal("0")
    for request in requested_lines:
        product = request["product"]
        quantity = Decimal(str(request["quantity"]))
        if quantity <= 0:
            raise ValueError("Dispensing quantity must be greater than zero.")
        if (
            product.organization_id != organization.id
            or product.pharmacy_id != order.pharmacy_id
        ):
            raise ValidationError("Dispensing product is outside the pharmacy scope.")
        _validate_product_matches_prescription(
            product=product, prescription=prescription
        )
        validate_controlled_dispensing(
            organization=organization,
            product=product,
            quantity=quantity,
            second_checker_id=request.get("second_checker_id"),
            actor_id=pharmacist_id,
        )
        requested_total += quantity

    if consumed + requested_total > maximum:
        raise ValidationError(
            f"Dispensing exceeds prescription allowance. Remaining quantity: {maximum - consumed}."
        )

    created = []
    for request in requested_lines:
        product = request["product"]
        quantity = Decimal(str(request["quantity"]))
        validate_controlled_dispensing(
            organization=organization,
            product=product,
            quantity=quantity,
            second_checker_id=request.get("second_checker_id"),
            actor_id=order.pharmacist_id,
        )
        movements = dispense_product(
            organization=organization,
            product=product,
            quantity=quantity,
            actor=order.pharmacist_id,
            reference_id=order.id,
        )
        for movement in movements:
            created.append(
                DispensingLine.objects.create(
                    dispensing_order=order,
                    product=product,
                    batch=movement.batch,
                    quantity_prescribed=quantity,
                    quantity_dispensed=movement.quantity,
                )
            )

    order.status = "dispensed"
    order.dispensed_at = timezone.now()
    order.save(update_fields=["status", "dispensed_at", "pharmacist_id", "updated_at"])
    record_audit(
        organization=organization,
        action="dispensing.completed",
        entity_type="DispensingOrder",
        entity_id=order.id,
        actor_id=order.pharmacist_id,
        payload={
            "prescription_id": str(prescription.id),
            "patient_id": str(getattr(prescription, "patient_id", "")),
            "quantity": str(requested_total),
            "remaining_prescription_quantity": str(
                maximum - consumed - requested_total
            ),
        },
    )
    return order, created


__all__ = (
    "create_dispensing_order",
    "dispense_order",
)
