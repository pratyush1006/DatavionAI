"""
Session selectors.
"""

from __future__ import annotations

import datetime
from uuid import UUID

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization
from apps.telemedicine.models import TelemedicineSession


class SessionSelector:
    """
    Read-only queries for telemedicine sessions.

    This selector centralizes all session retrieval logic.
    No write operations should be implemented here.
    """

    @staticmethod
    def queryset() -> QuerySet[TelemedicineSession]:
        """
        Return the base session queryset.
        """

        return TelemedicineSession.objects.select_related(
            "organization",
            "patient",
            "provider",
            "appointment",
        ).prefetch_related(
            "participants",
            "recordings",
        )

    @staticmethod
    def list() -> QuerySet[TelemedicineSession]:
        """
        Return all sessions.
        """

        return SessionSelector.queryset()

    @staticmethod
    def get(
        *,
        session_id: UUID,
    ) -> TelemedicineSession:
        """
        Return a session by identifier.
        """

        return get_object_or_404(
            SessionSelector.queryset(),
            pk=session_id,
        )

    @staticmethod
    def list_by_patient(
        *,
        patient_id: UUID,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return all sessions for a patient.
        """

        return SessionSelector.queryset().filter(
            patient_id=patient_id,
        )

    @staticmethod
    def list_by_provider(
        *,
        provider_id: UUID,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return all sessions for a provider.
        """

        return SessionSelector.queryset().filter(
            provider_id=provider_id,
        )

    @staticmethod
    def list_by_organization(
        *,
        organization: Organization,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return all sessions belonging to an organization.
        """

        return SessionSelector.queryset().filter(
            organization=organization,
        )

    @staticmethod
    def list_by_status(
        *,
        status: str,
        organization: Organization | None = None,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return sessions filtered by status.
        """

        queryset = SessionSelector.queryset().filter(
            status=status,
        )

        if organization is not None:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def list_by_date_range(
        *,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        organization: Organization | None = None,
    ) -> QuerySet[TelemedicineSession]:
        """
        Return sessions within a date range.
        """

        queryset = SessionSelector.queryset().filter(
            scheduled_start__gte=start_date,
            scheduled_start__lte=end_date,
        )

        if organization is not None:
            queryset = queryset.filter(
                organization=organization,
            )

        return queryset

    @staticmethod
    def search(
        *,
        organization: Organization,
        query: str,
    ) -> QuerySet[TelemedicineSession]:
        """
        Search sessions within an organization.
        """

        return (
            SessionSelector.queryset()
            .filter(
                organization=organization,
            )
            .filter(
                Q(
                    session_id__icontains=query,
                )
                | Q(
                    patient__first_name__icontains=query,
                )
                | Q(
                    patient__last_name__icontains=query,
                )
                | Q(
                    provider__employee__user__first_name__icontains=query,
                )
                | Q(
                    provider__employee__user__last_name__icontains=query,
                )
                | Q(
                    notes__icontains=query,
                )
            )
        )

    @staticmethod
    def count(
        *,
        organization: Organization | None = None,
        status: str | None = None,
    ) -> int:
        """
        Return the count of sessions matching the given filters.
        """

        queryset = SessionSelector.queryset()

        if organization is not None:
            queryset = queryset.filter(
                organization=organization,
            )

        if status is not None:
            queryset = queryset.filter(
                status=status,
            )

        return queryset.count()


# ---------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------

get_sessions = SessionSelector.list

get_session_by_id = SessionSelector.get

get_organization_sessions = SessionSelector.list_by_organization


__all__ = [
    "SessionSelector",
    "get_organization_sessions",
    "get_session_by_id",
    "get_sessions",
]
