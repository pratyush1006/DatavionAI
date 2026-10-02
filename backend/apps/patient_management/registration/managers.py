"""
Managers and querysets for the Patient Registration module.
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, cast

from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.patient_management.registration.constants import (
    RegistrationStatus,
)

if TYPE_CHECKING:
    from apps.patient_management.patients.models import Patient
    from apps.platform.organizations.models import Organization


class PatientRegistrationQuerySet(
    models.QuerySet,
):
    """
    QuerySet for PatientRegistration.

    Query methods are intentionally composable and do not perform
    authorization. Tenant and organization authorization belongs to the
    selector, policy, and workflow layers.
    """

    def active(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations that are currently active.

        Terminal lifecycle states are excluded:
        - COMPLETED
        - CANCELLED
        - REJECTED
        - NO_SHOW
        """

        return self.exclude(
            registration_status__in=(
                RegistrationStatus.COMPLETED,
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
                RegistrationStatus.NO_SHOW,
            ),
        )

    def completed(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return completed registrations.
        """

        return self.filter(
            registration_status=RegistrationStatus.COMPLETED,
        )

    def checked_in(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return checked-in registrations.
        """

        return self.filter(
            registration_status=RegistrationStatus.CHECKED_IN,
        )

    def verified(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return verified registrations.
        """

        return self.filter(
            verified=True,
        )

    def pending_verification(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations awaiting verification.
        """

        return self.filter(
            registration_status=RegistrationStatus.PENDING_VERIFICATION,
            verified=False,
        )

    def for_organization(
        self,
        organization: Organization,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations belonging to the organization.
        """

        return self.filter(
            organization=organization,
        )

    def for_patient(
        self,
        patient: Patient,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations belonging to the patient.
        """

        return self.filter(
            patient=patient,
        )

    def by_status(
        self,
        status: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter registrations by lifecycle status.
        """

        return self.filter(
            registration_status=status,
        )

    def by_type(
        self,
        registration_type: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter registrations by registration type.
        """

        return self.filter(
            registration_type=registration_type,
        )

    def by_source(
        self,
        source: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter registrations by registration source.
        """

        return self.filter(
            registration_source=source,
        )

    def by_priority(
        self,
        priority: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter registrations by registration priority.
        """

        return self.filter(
            priority=priority,
        )

    def today(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations for the current local date.
        """

        today = timezone.localdate()

        return self.filter(
            registration_datetime__date=today,
        )

    def this_week(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations during the current calendar week.
        """

        today = timezone.localdate()

        start = today - timedelta(
            days=today.weekday(),
        )

        end = start + timedelta(
            days=7,
        )

        return self.filter(
            registration_datetime__date__gte=start,
            registration_datetime__date__lt=end,
        )

    def this_month(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations during the current calendar month.
        """

        today = timezone.localdate()

        return self.filter(
            registration_datetime__year=today.year,
            registration_datetime__month=today.month,
        )

    def recent(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations ordered from newest to oldest.
        """

        return self.order_by(
            "-registration_datetime",
        )

    def needs_verification(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations that require verification.
        """

        return self.filter(
            registration_status=RegistrationStatus.PENDING_VERIFICATION,
            verified=False,
        )

    def ready_for_checkin(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return verified registrations that are eligible for check-in.

        VERIFIED is the canonical post-verification state.

        REGISTERED remains supported for existing or legacy records that
        may already be in that state.
        """

        return self.filter(
            verified=True,
            registration_status__in=(
                RegistrationStatus.VERIFIED,
                RegistrationStatus.REGISTERED,
            ),
        )

    def ready_for_completion(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations currently eligible for completion.
        """

        return self.filter(
            registration_status=RegistrationStatus.CHECKED_IN,
        )

    def search(
        self,
        query: str,
    ) -> PatientRegistrationQuerySet:
        """
        Search registrations by registration number or patient identity.
        """

        normalized_query = query.strip()

        if not normalized_query:
            return self

        return self.filter(
            Q(
                registration_number__icontains=normalized_query,
            )
            | Q(
                patient__mrn__icontains=normalized_query,
            )
            | Q(
                patient__first_name__icontains=normalized_query,
            )
            | Q(
                patient__last_name__icontains=normalized_query,
            ),
        )

    def by_registration_datetime(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations using the canonical registration ordering.
        """

        return self.order_by(
            "-registration_datetime",
        )

    def with_relations(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations with commonly required related objects loaded.
        """

        return self.select_related(
            "organization",
            "patient",
            "verified_by",
        )


class PatientRegistrationManager(
    models.Manager.from_queryset(
        PatientRegistrationQuerySet,
    ),
):  # type: ignore[misc]
    """
    Manager for PatientRegistration.

    The manager provides reusable query capabilities. Authorization and
    tenant-boundary enforcement remain outside the manager.
    """

    def get_queryset(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return the base optimized registration queryset.
        """

        return cast(
            PatientRegistrationQuerySet,
            super()
            .get_queryset()
            .select_related(
                "organization",
                "patient",
                "verified_by",
            ),
        )

    def active(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().active()

    def completed(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().completed()

    def checked_in(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().checked_in()

    def verified(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().verified()

    def pending_verification(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().pending_verification()

    def for_organization(
        self,
        organization: Organization,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().for_organization(
            organization,
        )

    def for_patient(
        self,
        patient: Patient,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().for_patient(
            patient,
        )

    def by_status(
        self,
        status: str,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().by_status(
            status,
        )

    def by_type(
        self,
        registration_type: str,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().by_type(
            registration_type,
        )

    def by_source(
        self,
        source: str,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().by_source(
            source,
        )

    def by_priority(
        self,
        priority: str,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().by_priority(
            priority,
        )

    def today(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().today()

    def this_week(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().this_week()

    def this_month(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().this_month()

    def recent(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().recent()

    def needs_verification(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().needs_verification()

    def ready_for_checkin(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().ready_for_checkin()

    def ready_for_completion(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().ready_for_completion()

    def search(
        self,
        query: str,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().search(
            query,
        )

    def by_registration_datetime(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().by_registration_datetime()

    def with_relations(
        self,
    ) -> PatientRegistrationQuerySet:
        return self.get_queryset().with_relations()


__all__ = (
    "PatientRegistrationManager",
    "PatientRegistrationQuerySet",
)
