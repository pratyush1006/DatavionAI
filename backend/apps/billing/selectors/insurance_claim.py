"""
InsuranceClaim selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.models import InsuranceClaim
from apps.platform.organizations.models import Organization


class InsuranceClaimSelector:
    """
    Read-only queries for insurance claims.

    This selector centralizes all insurance claim retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[InsuranceClaim]:
        """
        Return the base insurance claim queryset.
        """

        return InsuranceClaim.objects.select_related(
            "organization",
            "patient",
            "invoice",
        )

    @staticmethod
    def list() -> QuerySet[InsuranceClaim]:
        """
        Return all insurance claims.
        """

        return InsuranceClaimSelector.queryset()

    @staticmethod
    def get(
        *,
        claim_id: UUID,
    ) -> InsuranceClaim:
        """
        Return an insurance claim by identifier.
        """

        return get_object_or_404(
            InsuranceClaimSelector.queryset(),
            pk=claim_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[InsuranceClaim]:
        """
        Return claims for a specific patient.
        """

        return InsuranceClaimSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[InsuranceClaim]:
        """
        Return all claims belonging to an organization.
        """

        return InsuranceClaimSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_by_invoice(
        *,
        invoice_id: UUID,
    ) -> QuerySet[InsuranceClaim]:
        """
        Return claims for a specific invoice.
        """

        return InsuranceClaimSelector.queryset().filter(
            invoice_id=invoice_id,
        )

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[InsuranceClaim]:
        """
        Search insurance claims within an organization.
        """

        return (
            InsuranceClaimSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    claim_number__icontains=query,
                )
                | Q(
                    insurance_provider__icontains=query,
                )
                | Q(
                    policy_number__icontains=query,
                )
                | Q(
                    patient__first_name__icontains=query,
                )
                | Q(
                    patient__last_name__icontains=query,
                ),
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of insurance claims within an organization.
        """

        return InsuranceClaimSelector.list_by_organization(
            organization=organization,
        ).count()


# ---------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------

get_claims = InsuranceClaimSelector.list

get_claim_by_id = InsuranceClaimSelector.get

get_organization_claims = InsuranceClaimSelector.list_by_organization


__all__ = [
    "InsuranceClaimSelector",
    "get_claim_by_id",
    "get_claims",
    "get_organization_claims",
]
