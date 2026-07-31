"""
Prior Authorization selectors.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.revenue_cycle.prior_authorization.models import PriorAuthorizationRequest


class PriorAuthorizationRequestSelector:
    """
    Read-only queries for prior authorization records.
    """

    @staticmethod
    def queryset() -> QuerySet[PriorAuthorizationRequest]:
        return PriorAuthorizationRequest.objects.select_related(
            "organization",
            "patient",
        )

    @staticmethod
    def get(
        *,
        authorization_id: UUID,
    ) -> PriorAuthorizationRequest:
        return get_object_or_404(
            PriorAuthorizationRequestSelector.queryset(),
            pk=authorization_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[PriorAuthorizationRequest]:
        return PriorAuthorizationRequestSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[PriorAuthorizationRequest]:
        return PriorAuthorizationRequestSelector.queryset().filter(
            organization=organization,
        )


__all__ = [
    "PriorAuthorizationRequestSelector",
]
