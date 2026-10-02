"""Read selectors for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from .models import ARAccount, ARTransaction


class ARSelector:
    """Provide organization-scoped read operations."""

    @staticmethod
    def accounts(
        *,
        organization_id: UUID,
    ) -> QuerySet[ARAccount]:
        """Return active, non-deleted AR accounts for an organization."""

        return (
            ARAccount.objects.select_related("patient")
            .filter(organization_id=organization_id)
            .order_by("-created_at")
        )

    @staticmethod
    def account(
        *,
        organization_id: UUID,
        account_id: UUID,
    ) -> ARAccount:
        """Return one organization-scoped AR account."""

        return ARAccount.objects.select_related("patient").get(
            organization_id=organization_id,
            id=account_id,
        )

    @staticmethod
    def transactions(
        *,
        organization_id: UUID,
        account_id: UUID,
    ) -> QuerySet[ARTransaction]:
        """Return transactions for an organization-scoped AR account."""

        return ARTransaction.objects.filter(
            organization_id=organization_id,
            account_id=account_id,
        ).order_by("-transaction_date", "-created_at")


__all__ = ("ARSelector",)
