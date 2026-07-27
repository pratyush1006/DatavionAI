"""
Payment selectors.
"""

from __future__ import annotations

from datetime import date
from uuid import UUID

from django.db.models import QuerySet

from apps.billing.models import Payment
from apps.platform.organizations.models import Organization


class PaymentSelector:
    """
    Read-only queries for payments.

    This selector centralizes all payment retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[Payment]:
        """
        Return the base payment queryset.
        """

        return Payment.objects.select_related(
            "organization",
            "invoice",
            "patient",
            "received_by",
        )

    @staticmethod
    def list() -> QuerySet[Payment]:
        """
        Return all payments.
        """

        return PaymentSelector.queryset()

    @staticmethod
    def get(
        *,
        payment_id: UUID,
    ) -> Payment:
        """
        Return a payment by identifier.
        """

        from django.shortcuts import get_object_or_404

        return get_object_or_404(
            PaymentSelector.queryset(),
            pk=payment_id,
        )

    @staticmethod
    def list_by_invoice(
        *,
        invoice_id: UUID,
    ) -> QuerySet[Payment]:
        """
        Return payments for a specific invoice.
        """

        return PaymentSelector.queryset().filter(
            invoice_id=invoice_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[Payment]:
        """
        Return payments for a specific patient.
        """

        return PaymentSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Payment]:
        """
        Return all payments belonging to an organization.
        """

        return PaymentSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_by_date_range(
        *,
        organization: Organization,
        start_date: date,
        end_date: date,
    ) -> QuerySet[Payment]:
        """
        Return payments within a date range for an organization.
        """

        return PaymentSelector.queryset().filter(
            organization=organization,
            payment_date__gte=start_date,
            payment_date__lte=end_date,
        )


# ---------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------

get_payments = PaymentSelector.list

get_payment_by_id = PaymentSelector.get

get_organization_payments = PaymentSelector.list_by_organization


__all__ = [
    "PaymentSelector",
    "get_organization_payments",
    "get_payment_by_id",
    "get_payments",
]
