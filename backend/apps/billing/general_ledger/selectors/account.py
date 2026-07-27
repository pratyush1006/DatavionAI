"""
General Ledger selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.billing.general_ledger.constants import AccountStatus
from apps.billing.general_ledger.models import GeneralLedgerAccount
from apps.platform.organizations.models import Organization


class GeneralLedgerSelector:
    """
    Read-only queries for general ledger accounts.
    """

    @staticmethod
    def queryset() -> QuerySet[GeneralLedgerAccount]:
        """
        Return the base general ledger account queryset.
        """

        return GeneralLedgerAccount.objects.select_related(
            "organization",
            "parent",
        )

    @staticmethod
    def list() -> QuerySet[GeneralLedgerAccount]:
        """
        Return all general ledger accounts.
        """

        return GeneralLedgerSelector.queryset()

    @staticmethod
    def get(
        *,
        account_id: UUID,
    ) -> GeneralLedgerAccount:
        """
        Return a general ledger account by identifier.
        """

        return get_object_or_404(
            GeneralLedgerSelector.queryset(),
            pk=account_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[GeneralLedgerAccount]:
        """
        Return all general ledger accounts for an organization.
        """

        return GeneralLedgerSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_active(
        *,
        organization: Organization,
    ) -> QuerySet[GeneralLedgerAccount]:
        """
        Return active general ledger accounts.
        """

        return GeneralLedgerSelector.list_by_organization(
            organization=organization,
        ).filter(
            status=AccountStatus.ACTIVE,
        )

    @staticmethod
    def exists(
        *,
        organization: Organization,
        account_id: UUID,
    ) -> bool:
        """
        Determine whether a general ledger account exists.
        """

        return (
            GeneralLedgerSelector.list_by_organization(
                organization=organization,
            )
            .filter(
                pk=account_id,
            )
            .exists()
        )

    @staticmethod
    def count(
        *,
        organization: Organization,
    ) -> int:
        """
        Return the number of general ledger accounts for an organization.
        """

        return GeneralLedgerSelector.list_by_organization(
            organization=organization,
        ).count()


get_general_ledger_accounts = GeneralLedgerSelector.list

get_general_ledger_account_by_id = GeneralLedgerSelector.get

get_organization_general_ledger_accounts = GeneralLedgerSelector.list_by_organization


__all__ = [
    "GeneralLedgerSelector",
    "get_general_ledger_account_by_id",
    "get_general_ledger_accounts",
    "get_organization_general_ledger_accounts",
]
