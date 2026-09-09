"""
Billing Core Payment selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.billing.exceptions import BillingNotFoundError
from apps.billing.models import Payment


class PaymentSelector:
    """Provide tenant and organization scoped payment reads."""

    @staticmethod
    def queryset(
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> QuerySet[Payment]:
        """Return payments inside one tenant and organization."""
        return Payment.objects.select_related(
            "organization",
            "invoice",
            "patient",
            "received_by",
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
    ) -> QuerySet[Payment]:
        """List organization-scoped payments."""
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
        payment_id: UUID,
    ) -> Payment:
        """Retrieve one organization-scoped payment."""
        try:
            return cls.queryset(
                tenant_id=tenant_id,
                organization_id=organization_id,
            ).get(
                pk=payment_id,
            )
        except Payment.DoesNotExist as exc:
            raise BillingNotFoundError(
                "Payment was not found.",
            ) from exc


__all__ = ("PaymentSelector",)
