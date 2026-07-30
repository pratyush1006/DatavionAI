"""
SaaS Billing API filters.

DatavionOS billing query filters.

Supports:

- Billing Accounts
- Subscriptions
- Invoices
- Payments
- Usage Records
"""

from __future__ import annotations

import django_filters

from apps.platform.saas_billing.models import (
    BillingAccount,
    Invoice,
    Payment,
    Subscription,
    Usage,
)


class BillingAccountFilter(
    django_filters.FilterSet,
):
    """
    Billing account filtering.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    currency = django_filters.CharFilter(
        field_name="currency",
        lookup_expr="iexact",
    )

    class Meta:
        model = BillingAccount

        fields = [
            "status",
            "currency",
        ]


class SubscriptionFilter(
    django_filters.FilterSet,
):
    """
    Subscription filtering.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    plan = django_filters.UUIDFilter(
        field_name="plan_id",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization_id",
    )

    class Meta:
        model = Subscription

        fields = [
            "status",
            "plan",
            "organization",
        ]


class InvoiceFilter(
    django_filters.FilterSet,
):
    """
    Invoice filtering.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    invoice_type = django_filters.CharFilter(
        field_name="invoice_type",
        lookup_expr="iexact",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization_id",
    )

    date_from = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    date_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Invoice

        fields = [
            "status",
            "invoice_type",
            "organization",
            "date_from",
            "date_to",
        ]


class PaymentFilter(
    django_filters.FilterSet,
):
    """
    Payment filtering.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="iexact",
    )

    provider = django_filters.CharFilter(
        field_name="provider",
        lookup_expr="iexact",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization_id",
    )

    date_from = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    date_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Payment

        fields = [
            "status",
            "provider",
            "organization",
            "date_from",
            "date_to",
        ]


class UsageFilter(
    django_filters.FilterSet,
):
    """
    Usage metering filtering.
    """

    metric_type = django_filters.CharFilter(
        field_name="metric_type",
        lookup_expr="iexact",
    )

    billable = django_filters.BooleanFilter(
        field_name="is_billable",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization_id",
    )

    date_from = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    date_to = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Usage

        fields = [
            "metric_type",
            "billable",
            "organization",
            "date_from",
            "date_to",
        ]


__all__ = (
    "BillingAccountFilter",
    "SubscriptionFilter",
    "InvoiceFilter",
    "PaymentFilter",
    "UsageFilter",
)
