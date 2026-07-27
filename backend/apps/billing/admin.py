"""
Admin configuration for the Billing application.
"""

from __future__ import annotations

from django.contrib import admin

from apps.billing.models import InsuranceClaim, Invoice, InvoiceItem, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Invoice.
    """

    list_display = (
        "invoice_number",
        "organization",
        "patient",
        "invoice_date",
        "due_date",
        "total_amount",
        "paid_amount",
        "balance_amount",
        "status",
        "is_active",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "patient__first_name",
        "patient__last_name",
        "notes",
    )

    list_filter = (
        "organization",
        "status",
        "invoice_date",
        "due_date",
        "is_active",
    )

    ordering = (
        "-invoice_date",
        "-created_at",
    )

    readonly_fields = (
        "id",
        "paid_amount",
        "balance_amount",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
    )

    list_select_related = (
        "organization",
        "patient",
    )

    list_per_page = 25

    date_hierarchy = "invoice_date"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Invoice Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "invoice_number",
                    "invoice_date",
                    "due_date",
                ),
            },
        ),
        (
            "Financial Details",
            {
                "fields": (
                    "total_amount",
                    "paid_amount",
                    "balance_amount",
                    "status",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("notes",),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    """
    Django admin configuration for InvoiceItem.
    """

    list_display = (
        "description",
        "invoice",
        "quantity",
        "unit_price",
        "total_price",
        "service_code",
        "is_active",
        "created_at",
    )

    search_fields = (
        "description",
        "service_code",
        "invoice__invoice_number",
    )

    list_filter = (
        "invoice",
        "service_code",
        "is_active",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "total_price",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("invoice",)

    list_select_related = ("invoice",)

    list_per_page = 25

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Item Information",
            {
                "fields": (
                    "invoice",
                    "description",
                    "quantity",
                    "unit_price",
                    "total_price",
                    "service_code",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Payment.
    """

    list_display = (
        "id",
        "organization",
        "invoice",
        "patient",
        "payment_method",
        "amount",
        "payment_date",
        "reference_number",
        "is_active",
        "created_at",
    )

    search_fields = (
        "invoice__invoice_number",
        "patient__first_name",
        "patient__last_name",
        "reference_number",
        "notes",
    )

    list_filter = (
        "organization",
        "payment_method",
        "payment_date",
        "is_active",
    )

    ordering = (
        "-payment_date",
        "-created_at",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "invoice",
        "patient",
        "received_by",
    )

    list_select_related = (
        "organization",
        "invoice",
        "patient",
        "received_by",
    )

    list_per_page = 25

    date_hierarchy = "payment_date"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "organization",
                    "invoice",
                    "patient",
                    "payment_method",
                    "amount",
                    "payment_date",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "reference_number",
                    "notes",
                    "received_by",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    """
    Django admin configuration for InsuranceClaim.
    """

    list_display = (
        "claim_number",
        "organization",
        "patient",
        "invoice",
        "insurance_provider",
        "policy_number",
        "claim_amount",
        "approved_amount",
        "status",
        "is_active",
        "created_at",
    )

    search_fields = (
        "claim_number",
        "insurance_provider",
        "policy_number",
        "patient__first_name",
        "patient__last_name",
        "rejection_reason",
    )

    list_filter = (
        "organization",
        "status",
        "insurance_provider",
        "is_active",
    )

    ordering = (
        "-submitted_at",
        "-created_at",
    )

    readonly_fields = (
        "id",
        "submitted_at",
        "settled_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "organization",
        "patient",
        "invoice",
    )

    list_select_related = (
        "organization",
        "patient",
        "invoice",
    )

    list_per_page = 25

    date_hierarchy = "submitted_at"

    preserve_filters = True

    empty_value_display = "-"

    fieldsets = (
        (
            "Claim Information",
            {
                "fields": (
                    "organization",
                    "patient",
                    "invoice",
                    "insurance_provider",
                    "policy_number",
                    "claim_number",
                ),
            },
        ),
        (
            "Financial Details",
            {
                "fields": (
                    "claim_amount",
                    "approved_amount",
                    "status",
                ),
            },
        ),
        (
            "Status Information",
            {
                "fields": (
                    "submitted_at",
                    "settled_at",
                    "rejection_reason",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


__all__ = [
    "InvoiceAdmin",
    "InvoiceItemAdmin",
    "InsuranceClaimAdmin",
    "PaymentAdmin",
]
