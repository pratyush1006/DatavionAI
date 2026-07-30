"""
AR Record selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.ar.models import AccountsReceivable


class AccountsReceivableSelector:
    """
    Read-only queries for ar record records.
    """

    @staticmethod
    def queryset() -> QuerySet[AccountsReceivable]:
        return AccountsReceivable.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        ar_id: UUID,
    ) -> AccountsReceivable:
        return get_object_or_404(
            AccountsReceivableSelector.queryset(),
            pk=ar_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[AccountsReceivable]:
        return AccountsReceivableSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[AccountsReceivable]:
        return AccountsReceivableSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "AccountsReceivableSelector",
]
