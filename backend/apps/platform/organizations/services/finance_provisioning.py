from __future__ import annotations

from datetime import date
from typing import Any

from django.apps import apps
from django.db import transaction


def _get_fiscal_period_model() -> type[Any]:
    """Resolve the canonical FiscalPeriod model through Django's registry."""

    return apps.get_model(
        "finance",
        "FiscalPeriod",
    )


def _resolve_fiscal_period_model() -> type[Any]:
    """Resolve FiscalPeriod without assuming a models.py layout."""

    try:
        return _get_fiscal_period_model()
    except LookupError:
        pass

    matches: list[type[Any]] = []

    for model in apps.get_models():
        if model.__name__ == "FiscalPeriod":
            matches.append(model)

    if not matches:
        raise LookupError("Canonical FiscalPeriod model could not be resolved.")

    if len(matches) > 1:
        labels = ", ".join(model._meta.label for model in matches)
        raise LookupError(f"Multiple FiscalPeriod models were found: {labels}")

    return matches[0]


def provision_organization_finance(
    *,
    organization: Any,
    effective_date: date | None = None,
) -> Any:
    """Provision the current enterprise-finance fiscal period.

    This function owns only the organization -> finance bootstrap boundary.

    It deliberately does NOT create:
      * SaaS subscriptions
      * SaaS invoices
      * healthcare billing records
      * Family Members records

    The operation is idempotent and safe to call repeatedly.
    """

    if organization is None:
        raise ValueError("organization is required")

    if getattr(organization, "pk", None) is None:
        raise ValueError("organization must be persisted before finance provisioning")

    fiscal_period_model = _resolve_fiscal_period_model()

    target_date = effective_date or date.today()

    fiscal_year = target_date.year
    period_number = target_date.month

    period_start = target_date.replace(day=1)

    if period_number == 12:
        next_month = target_date.replace(
            year=target_date.year + 1,
            month=1,
            day=1,
        )
    else:
        next_month = target_date.replace(
            month=target_date.month + 1,
            day=1,
        )

    period_end = next_month.fromordinal(next_month.toordinal() - 1)

    defaults = {
        "period_start": period_start,
        "period_end": period_end,
        "status": "open",
    }

    with transaction.atomic():
        fiscal_period, created = fiscal_period_model.objects.get_or_create(
            organization=organization,
            fiscal_year=fiscal_year,
            period=period_number,
            defaults=defaults,
        )

        if not created:
            return fiscal_period

        return fiscal_period


__all__ = [
    "provision_organization_finance",
]
