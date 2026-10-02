from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.pharmacy.models import PharmacyReturn, PharmacyReturnLine
from apps.pharmacy.services.inventory import return_stock


@transaction.atomic
def create_pharmacy_return(
    *,
    organization,
    return_type,
    return_number,
    reason,
    lines,
    dispensing_order=None,
    purchase_order=None,
    actor_id=None,
):
    if not lines:
        raise ValidationError("At least one return line is required.")
    if return_type == "patient" and dispensing_order is None:
        raise ValidationError("Patient returns require a dispensing order.")
    if return_type == "supplier" and purchase_order is None:
        raise ValidationError("Supplier returns require a purchase order.")
    if (
        dispensing_order is not None
        and dispensing_order.organization_id != organization.id
    ):
        raise ValidationError("Dispensing order is outside the organization scope.")
    if purchase_order is not None and purchase_order.organization_id != organization.id:
        raise ValidationError("Purchase order is outside the organization scope.")

    result = PharmacyReturn.objects.create(
        return_type=return_type,
        return_number=return_number,
        reason=reason,
        dispensing_order=dispensing_order,
        purchase_order=purchase_order,
        processed_by_id=getattr(actor_id, "pk", actor_id) if actor_id else None,
    )
    for item in lines:
        product = item["product"]
        batch = item["batch"]
        quantity = Decimal(str(item["quantity"]))
        restockable = bool(item.get("restockable", False))
        if product.organization_id != organization.id or batch.product_id != product.id:
            raise ValidationError(
                "Return inventory is outside the organization/product scope."
            )
        if quantity <= 0:
            raise ValidationError("Return quantity must be greater than zero.")
        PharmacyReturnLine.objects.create(
            pharmacy_return=result,
            product=product,
            batch=batch,
            quantity=quantity,
            restockable=restockable,
        )
        return_stock(
            organization=organization,
            batch=batch,
            quantity=quantity,
            restockable=restockable,
            actor=actor_id,
            reference_type="PharmacyReturn",
            reference_id=result.id,
            note=reason,
        )
    return result
