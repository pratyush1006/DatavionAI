"""Live organization-scoped Finance Manager dashboard projection."""

from __future__ import annotations

from calendar import monthrange
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.common.finance.currency import DEFAULT_CURRENCY
from apps.revenue_cycle.billing.models.healthcare_models import (
    HealthcareInvoice,
    HealthcarePayment,
)
from apps.revenue_cycle.denials.constants import DenialStatus
from apps.revenue_cycle.denials.models import Denial

ZERO = Decimal("0.00")
BILLABLE_INVOICE_STATUSES = (
    HealthcareInvoice.Status.FINALIZED,
    HealthcareInvoice.Status.PARTIALLY_PAID,
    HealthcareInvoice.Status.PAID,
    HealthcareInvoice.Status.WRITTEN_OFF,
)
OPEN_INVOICE_STATUSES = (
    HealthcareInvoice.Status.FINALIZED,
    HealthcareInvoice.Status.PARTIALLY_PAID,
)
OPEN_DENIAL_STATUSES = (
    DenialStatus.OPEN,
    DenialStatus.UNDER_REVIEW,
    DenialStatus.ACTION_REQUIRED,
    DenialStatus.APPEAL_PENDING,
)


def _previous_month(value: date) -> date:
    if value.month == 1:
        return date(value.year - 1, 12, 1)
    return date(value.year, value.month - 1, 1)


def _aware_midnight(value: date):
    return timezone.make_aware(
        datetime.combine(value, time.min),
        timezone.get_current_timezone(),
    )


def _sum_by_currency(
    queryset, amount_field: str, currency_field: str = "currency"
) -> dict[str, Decimal]:
    rows = queryset.values(currency_field).annotate(total=Sum(amount_field))
    return {str(row[currency_field]): row["total"] or ZERO for row in rows}


def build_finance_dashboard(
    *, organization: Any, today: date | None = None
) -> dict[str, Any]:
    """Aggregate current healthcare billing and denial data by currency."""
    as_of = today or timezone.localdate()
    month_start = as_of.replace(day=1)
    previous_month_start = _previous_month(month_start)
    current_start_at = _aware_midnight(month_start)
    current_end_at = timezone.now()
    previous_month_elapsed_days = min(
        as_of.day,
        monthrange(previous_month_start.year, previous_month_start.month)[1],
    )
    previous_end_at = _aware_midnight(
        previous_month_start + timedelta(days=previous_month_elapsed_days)
    )
    trend_start = month_start
    for _ in range(5):
        trend_start = _previous_month(trend_start)
    trend_start_at = _aware_midnight(trend_start)

    invoices = HealthcareInvoice.objects.filter(
        organization=organization,
        status__in=BILLABLE_INVOICE_STATUSES,
        finalized_at__isnull=False,
    )
    current_invoices = invoices.filter(
        finalized_at__gte=current_start_at,
        finalized_at__lt=current_end_at,
    )
    previous_invoices = invoices.filter(
        finalized_at__gte=_aware_midnight(previous_month_start),
        finalized_at__lt=previous_end_at,
    )
    open_invoices = invoices.filter(
        status__in=OPEN_INVOICE_STATUSES,
        balance_due__gt=ZERO,
    )
    overdue_invoices = open_invoices.filter(due_date__lt=as_of)
    payments = HealthcarePayment.objects.filter(
        organization=organization,
        invoice__organization=organization,
        status=HealthcarePayment.Status.POSTED,
        posted_at__gte=current_start_at,
        posted_at__lt=current_end_at,
    )

    revenue_by_currency = _sum_by_currency(current_invoices, "total")
    previous_revenue_by_currency = _sum_by_currency(previous_invoices, "total")
    collected_by_currency = _sum_by_currency(payments, "amount", "invoice__currency")
    outstanding_by_currency = _sum_by_currency(open_invoices, "balance_due")
    overdue_amount_by_currency = _sum_by_currency(overdue_invoices, "balance_due")
    overdue_count_by_currency = {
        str(row["currency"]): row["count"]
        for row in overdue_invoices.values("currency").annotate(count=Count("id"))
    }

    trend_rows = (
        invoices.filter(
            finalized_at__gte=trend_start_at, finalized_at__lt=current_end_at
        )
        .annotate(
            month=TruncMonth("finalized_at", tzinfo=timezone.get_current_timezone())
        )
        .values("currency", "month")
        .annotate(amount=Sum("total"))
        .order_by("month", "currency")
    )
    trend = [
        {
            "month": row["month"].date().isoformat(),
            "currency": str(row["currency"]),
            "amount": str(row["amount"] or ZERO),
        }
        for row in trend_rows
    ]

    currencies = sorted(
        set(revenue_by_currency)
        | set(collected_by_currency)
        | set(outstanding_by_currency)
        | set(overdue_amount_by_currency)
    ) or [DEFAULT_CURRENCY]
    currency_totals = []
    for currency in currencies:
        revenue = revenue_by_currency.get(currency, ZERO)
        collected = collected_by_currency.get(currency, ZERO)
        previous_revenue = previous_revenue_by_currency.get(currency, ZERO)
        change_percent = (
            round(float((revenue - previous_revenue) / previous_revenue * 100), 1)
            if previous_revenue > ZERO
            else None
        )
        collection_rate = (
            round(float(collected / revenue * 100), 1) if revenue > ZERO else None
        )
        currency_totals.append(
            {
                "currency": currency,
                "revenue_mtd": str(revenue),
                "revenue_previous_month": str(previous_revenue),
                "revenue_change_percent": change_percent,
                "collected_mtd": str(collected),
                "collection_rate_percent": collection_rate,
                "outstanding": str(outstanding_by_currency.get(currency, ZERO)),
                "overdue_amount": str(overdue_amount_by_currency.get(currency, ZERO)),
                "overdue_invoice_count": overdue_count_by_currency.get(currency, 0),
            }
        )

    open_denials = Denial.objects.filter(
        organization=organization,
        status__in=OPEN_DENIAL_STATUSES,
    ).count()
    recent_invoices = [
        {
            "invoice_number": row["invoice_number"],
            "payer_name": row["payer_name"],
            "claim_reference": row["claim_reference"],
            "currency": row["currency"],
            "status": row["status"],
            "total": str(row["total"] or ZERO),
            "balance_due": str(row["balance_due"] or ZERO),
            "due_date": row["due_date"].isoformat() if row["due_date"] else None,
        }
        for row in invoices.order_by("-finalized_at").values(
            "invoice_number",
            "payer_name",
            "claim_reference",
            "currency",
            "status",
            "total",
            "balance_due",
            "due_date",
        )[:25]
    ]
    return {
        "as_of": as_of.isoformat(),
        "period_start": month_start.isoformat(),
        "period_end": as_of.isoformat(),
        "currency_totals": currency_totals,
        "trend": trend,
        "recent_invoices": recent_invoices,
        "alerts": {
            "overdue_invoice_count": sum(overdue_count_by_currency.values()),
            "open_denial_count": open_denials,
        },
    }


__all__ = ("build_finance_dashboard",)
