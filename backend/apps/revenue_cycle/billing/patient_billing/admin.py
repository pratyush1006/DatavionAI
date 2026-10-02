"""Patient Billing Django admin registrations."""

from __future__ import annotations

from django.contrib import admin

from apps.revenue_cycle.billing.patient_billing.models import (
    PatientBillingAccount,
    PatientBillingStatement,
    PatientFinancialResponsibility,
    PatientGuarantor,
)


@admin.register(PatientBillingAccount)
class PatientBillingAccountAdmin(admin.ModelAdmin):
    """Admin configuration for patient billing accounts."""

    list_display = (
        "account_number",
        "organization",
        "patient",
        "status",
        "currency",
        "current_balance",
    )
    list_filter = (
        "status",
        "currency",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "account_number",
        "patient__first_name",
        "patient__last_name",
        "patient__mrn",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
        "deleted_by_id",
    )


@admin.register(PatientGuarantor)
class PatientGuarantorAdmin(admin.ModelAdmin):
    """Admin configuration for patient guarantors."""

    list_display = (
        "name",
        "patient",
        "organization",
        "relationship",
        "is_primary",
        "is_active",
    )
    list_filter = (
        "relationship",
        "is_primary",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "name",
        "phone",
        "email",
        "patient__mrn",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
        "deleted_by_id",
    )


@admin.register(PatientFinancialResponsibility)
class PatientFinancialResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for financial responsibility."""

    list_display = (
        "account",
        "party_type",
        "guarantor",
        "percentage",
        "priority",
        "is_active",
    )
    list_filter = (
        "party_type",
        "is_active",
        "is_deleted",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
        "deleted_by_id",
    )


@admin.register(PatientBillingStatement)
class PatientBillingStatementAdmin(admin.ModelAdmin):
    """Admin configuration for patient billing statements."""

    list_display = (
        "statement_number",
        "account",
        "period_start",
        "period_end",
        "closing_balance",
        "status",
    )
    list_filter = (
        "status",
        "is_deleted",
    )
    search_fields = (
        "statement_number",
        "account__account_number",
        "account__patient__mrn",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "issued_at",
        "deleted_at",
        "deleted_by_id",
    )


__all__ = (
    "PatientBillingAccountAdmin",
    "PatientBillingStatementAdmin",
    "PatientFinancialResponsibilityAdmin",
    "PatientGuarantorAdmin",
)
