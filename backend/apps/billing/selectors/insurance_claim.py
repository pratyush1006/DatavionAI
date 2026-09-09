"""
Billing Core insurance claim selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.billing.exceptions import BillingNotFoundError
from apps.billing.models import InsuranceClaim


class InsuranceClaimSelector:
    """Provide tenant and organization scoped claim reads."""

    @staticmethod
    def queryset(
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> QuerySet[InsuranceClaim]:
        """Return claims inside one tenant and organization."""
        return InsuranceClaim.objects.select_related(
            "organization",
            "patient",
            "invoice",
        ).filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )

    @classmethod
    def list(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> QuerySet[InsuranceClaim]:
        """List organization-scoped claims."""
        return cls.queryset(
            tenant_id=tenant_id,
            organization_id=organization_id,
        )

    @classmethod
    def get(
        cls,
        *,
        tenant_id: UUID,
        organization_id: UUID,
        claim_id: UUID,
    ) -> InsuranceClaim:
        """Retrieve one organization-scoped claim."""
        try:
            return cls.queryset(
                tenant_id=tenant_id,
                organization_id=organization_id,
            ).get(
                pk=claim_id,
            )
        except InsuranceClaim.DoesNotExist as exc:
            raise BillingNotFoundError(
                "Insurance claim was not found.",
            ) from exc


__all__ = ("InsuranceClaimSelector",)
