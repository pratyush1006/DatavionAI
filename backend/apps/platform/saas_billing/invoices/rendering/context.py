"""
Dynamic invoice rendering context.

This module deliberately does not define database models.

Invoice data is supplied by the canonical SaaS billing layer.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

_MISSING = object()


def value(
    source: Any,
    *names: str,
    default: Any = None,
) -> Any:
    """
    Read a value from mappings or objects.

    Supports both:
    - dictionary-style invoice contexts
    - Django/domain objects
    """

    current = source

    for name in names:
        if current is None:
            return default

        if isinstance(current, Mapping):
            current = current.get(
                name,
                _MISSING,
            )

        else:
            current = getattr(
                current,
                name,
                _MISSING,
            )

        if current is _MISSING:
            return default

    return current


def as_decimal_string(
    amount: Any,
    default: str = "0.00",
) -> str:
    """
    Format monetary values without introducing
    business calculations into the presentation layer.
    """

    if amount is None:
        return default

    try:
        return f"{float(amount):,.2f}"
    except (TypeError, ValueError):
        return str(amount)


def build_invoice_context(
    invoice: Any,
    *,
    seller: Mapping[str, Any] | None = None,
    customer: Mapping[str, Any] | None = None,
    branding: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build a presentation context from canonical billing data.

    The function does not calculate tax, pricing, discounts,
    or subscription charges. Those values must already come
    from the billing domain.
    """

    seller_data = dict(seller or {})
    customer_data = dict(customer or {})
    branding_data = dict(branding or {})

    line_items = value(
        invoice,
        "line_items",
        "items",
        default=[],
    )

    taxes = value(
        invoice,
        "taxes",
        default=[],
    )

    discounts = value(
        invoice,
        "discounts",
        default=[],
    )

    totals = value(
        invoice,
        "totals",
        default={},
    )

    payment = value(
        invoice,
        "payment",
        default={},
    )

    subscription = value(
        invoice,
        "subscription",
        default={},
    )

    plan = value(
        subscription,
        "plan",
        default={},
    )

    return {
        "seller": seller_data,
        "customer": customer_data,
        "branding": branding_data,
        "invoice": {
            "number": value(
                invoice,
                "number",
                "invoice_number",
            ),
            "issue_date": value(
                invoice,
                "issue_date",
                "issued_at",
                "created_at",
            ),
            "due_date": value(
                invoice,
                "due_date",
            ),
            "status": value(
                invoice,
                "status",
            ),
            "currency": value(
                invoice,
                "currency",
                default="INR",
            ),
            "billing_period_start": value(
                invoice,
                "billing_period_start",
            ),
            "billing_period_end": value(
                invoice,
                "billing_period_end",
            ),
            "type": value(
                invoice,
                "invoice_type",
                "type",
            ),
        },
        "subscription": {
            "id": value(
                subscription,
                "id",
                "uuid",
            ),
            "plan_name": value(
                subscription,
                "plan_name",
                default=value(
                    plan,
                    "name",
                ),
            ),
            "status": value(
                subscription,
                "status",
            ),
        },
        "line_items": line_items,
        "discounts": discounts,
        "taxes": taxes,
        "totals": totals,
        "payment": payment,
    }


__all__ = (
    "build_invoice_context",
    "as_decimal_string",
    "value",
)
