"""
DatavionOS SaaS Billing admin configuration.

Provides enterprise admin interfaces for:

- Billing Accounts
- Subscription Plans
- Subscriptions
- Invoices
- Payments
- Usage Records
"""

from django.contrib import admin

from apps.platform.saas_billing.models import (
    BillingAccount,
    Invoice,
    Payment,
    Plan,
    Subscription,
    Usage,
)


@admin.register(BillingAccount)
class BillingAccountAdmin(admin.ModelAdmin):
    """
    Billing account administration.
    """

    list_display = (
        "organization",
        "status",
        "currency",
        "payment_provider",
        "auto_charge_enabled",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "payment_provider",
        "auto_charge_enabled",
    )

    search_fields = (
        "organization__name",
        "legal_name",
        "billing_email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    SaaS plan administration.
    """

    list_display = (
        "name",
        "code",
        "plan_type",
        "healthcare_segment",
        "price",
        "currency",
        "billing_cycle",
        "is_active",
        "is_public",
    )

    list_filter = (
        "plan_type",
        "healthcare_segment",
        "billing_cycle",
        "currency",
        "is_active",
        "is_public",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Subscription lifecycle administration.
    """

    list_display = (
        "organization",
        "plan",
        "status",
        "current_period_start",
        "current_period_end",
        "auto_renew",
        "created_at",
    )

    list_filter = (
        "status",
        "auto_renew",
        "plan",
    )

    search_fields = (
        "organization__name",
        "plan__name",
        "external_subscription_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    SaaS invoice administration.
    """

    list_display = (
        "invoice_number",
        "organization",
        "invoice_type",
        "status",
        "total_amount",
        "currency",
        "issued_at",
        "due_at",
    )

    list_filter = (
        "status",
        "invoice_type",
        "currency",
    )

    search_fields = (
        "invoice_number",
        "organization__name",
        "external_invoice_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Payment transaction administration.
    """

    list_display = (
        "organization",
        "invoice",
        "amount",
        "currency",
        "provider",
        "status",
        "paid_at",
        "created_at",
    )

    list_filter = (
        "status",
        "provider",
        "payment_method",
        "currency",
    )

    search_fields = (
        "organization__name",
        "transaction_id",
        "gateway_payment_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    """
    Usage metering administration.
    """

    list_display = (
        "organization",
        "metric_type",
        "value",
        "unit",
        "is_billable",
        "calculated_cost",
        "created_at",
    )

    list_filter = (
        "metric_type",
        "is_billable",
        "source",
    )

    search_fields = (
        "organization__name",
        "reference_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
