"""
Invoice selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.models import Invoice
from apps.platform.organizations.models import Organization


class InvoiceSelector:
    """
    Read-only queries for invoices.

    This selector centralizes all invoice retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[Invoice]:
        """
        Return the base invoice queryset.
        """

        return Invoice.objects.select_related(
            "organization",
            "patient",
        ).prefetch_related(
            "items",
            "payments",
            "insurance_claims",
        )

    @staticmethod
    def list() -> QuerySet[Invoice]:
        """
        Return all invoices.
        """

        return InvoiceSelector.queryset()

    @staticmethod
    def get(
        *,
        invoice_id: UUID,
    ) -> Invoice:
        """
        Return an invoice by identifier.
        """

        return get_object_or_404(
            InvoiceSelector.queryset(),
            pk=invoice_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[Invoice]:
        """
        Return invoices for a specific patient.
        """

        return InvoiceSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[Invoice]:
        """
        Return all invoices belonging to an organization.
        """

        return InvoiceSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[Invoice]:
        """
        Search invoices within an organization.
        """

        return (
            InvoiceSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    invoice_number__icontains=query,
                )
                | Q(
                    patient__first_name__icontains=query,
                )
                | Q(
                    patient__last_name__icontains=query,
                )
                | Q(
                    notes__icontains=query,
                ),
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of invoices within an organization.
        """

        return InvoiceSelector.list_by_organization(
            organization=organization,
        ).count()

    @staticmethod
    def list_overdue(
        *,
        organization: Organization,
    ) -> QuerySet[Invoice]:
        """
        Return overdue invoices for an organization.
        """

        from django.utils import timezone

        return InvoiceSelector.queryset().filter(
            organization=organization,
            balance_amount__gt=0,
            due_date__lt=timezone.now().date(),
        )


# ---------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------

get_invoices = InvoiceSelector.list

get_invoice_by_id = InvoiceSelector.get

get_organization_invoices = InvoiceSelector.list_by_organization


__all__ = [
    "InvoiceSelector",
    "get_invoice_by_id",
    "get_invoices",
    "get_organization_invoices",
]
