"""
Managers for the Patient Registration module.
"""

from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.patient_management.registration.constants import (
    RegistrationStatus,
)


class PatientRegistrationQuerySet(
    models.QuerySet,
):
    """
    QuerySet for PatientRegistration.
    """

    def active(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return active registrations.
        """

        return self.exclude(
            registration_status__in=(
                RegistrationStatus.CANCELLED,
                RegistrationStatus.REJECTED,
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
            registration_status=(RegistrationStatus.PENDING_VERIFICATION),
        )

    def for_organization(
        self,
        organization,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by organization.
        """

        return self.filter(
            organization=organization,
        )

    def for_patient(
        self,
        patient,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by patient.
        """

        return self.filter(
            patient=patient,
        )

    def by_status(
        self,
        status: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by registration status.
        """

        return self.filter(
            registration_status=status,
        )

    def by_type(
        self,
        registration_type: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by registration type.
        """

        return self.filter(
            registration_type=registration_type,
        )

    def by_source(
        self,
        source: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by registration source.
        """

        return self.filter(
            registration_source=source,
        )

    def by_priority(
        self,
        priority: str,
    ) -> PatientRegistrationQuerySet:
        """
        Filter by priority.
        """

        return self.filter(
            priority=priority,
        )

    def today(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return today's registrations.
        """

        today = timezone.localdate()

        return self.filter(
            registration_datetime__date=today,
        )

    def this_week(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return this week's registrations.
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
        Return this month's registrations.
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
        Return registrations ordered by most recent.
        """

        return self.order_by(
            "-registration_datetime",
        )

    def needs_verification(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations requiring verification.
        """

        return self.filter(
            verified=False,
            registration_status=(RegistrationStatus.PENDING_VERIFICATION),
        )

    def ready_for_checkin(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations ready for check-in.
        """

        return self.filter(
            registration_status=RegistrationStatus.REGISTERED,
            verified=True,
        )

    def ready_for_completion(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return registrations ready for completion.
        """

        return self.filter(
            registration_status=RegistrationStatus.CHECKED_IN,
        )

    def search(
        self,
        query: str,
    ) -> PatientRegistrationQuerySet:
        """
        Search registrations.
        """

        if not query:
            return self

        return self.filter(
            Q(
                registration_number__icontains=query,
            )
            | Q(
                patient__medical_record_number__icontains=query,
            )
            | Q(
                patient__first_name__icontains=query,
            )
            | Q(
                patient__last_name__icontains=query,
            ),
        )


class PatientRegistrationManager(
    models.Manager.from_queryset(
        PatientRegistrationQuerySet,
    ),
):
    """
    Manager for PatientRegistration.
    """

    def get_queryset(
        self,
    ) -> PatientRegistrationQuerySet:
        """
        Return the optimized queryset.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "organization",
                "patient",
                "verified_by",
            )
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
