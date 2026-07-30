"""
Filters for the Patient Registration module.
"""

from __future__ import annotations

import django_filters
from apps.patient_management.registration.models import (
    PatientRegistration,
)


class PatientRegistrationFilter(
    django_filters.FilterSet,
):
    """
    FilterSet for PatientRegistration.
    """

    registration_number = django_filters.CharFilter(
        field_name="registration_number",
        lookup_expr="icontains",
    )

    patient = django_filters.UUIDFilter(
        field_name="patient__uuid",
    )

    organization = django_filters.UUIDFilter(
        field_name="organization__uuid",
    )

    registration_type = django_filters.CharFilter(
        field_name="registration_type",
    )

    registration_status = django_filters.CharFilter(
        field_name="registration_status",
    )

    registration_source = django_filters.CharFilter(
        field_name="registration_source",
    )

    visit_type = django_filters.CharFilter(
        field_name="visit_type",
    )

    priority = django_filters.CharFilter(
        field_name="priority",
    )

    verified = django_filters.BooleanFilter(
        field_name="verified",
    )

    registration_datetime_after = django_filters.DateTimeFilter(
        field_name="registration_datetime",
        lookup_expr="gte",
    )

    registration_datetime_before = django_filters.DateTimeFilter(
        field_name="registration_datetime",
        lookup_expr="lte",
    )

    #
    # Enterprise Filters
    #

    search = django_filters.CharFilter(
        method="filter_search",
    )

    today = django_filters.BooleanFilter(
        method="filter_today",
    )

    this_week = django_filters.BooleanFilter(
        method="filter_this_week",
    )

    this_month = django_filters.BooleanFilter(
        method="filter_this_month",
    )

    active = django_filters.BooleanFilter(
        method="filter_active",
    )

    needs_verification = django_filters.BooleanFilter(
        method="filter_needs_verification",
    )

    ready_for_checkin = django_filters.BooleanFilter(
        method="filter_ready_for_checkin",
    )

    ready_for_completion = django_filters.BooleanFilter(
        method="filter_ready_for_completion",
    )

    class Meta:
        model = PatientRegistration

        fields = (
            "organization",
            "patient",
            "registration_number",
            "registration_type",
            "registration_status",
            "registration_source",
            "visit_type",
            "priority",
            "verified",
        )

    def filter_search(
        self,
        queryset,
        name,
        value,
    ):
        """
        Search registrations.
        """

        return queryset.search(
            value,
        )

    def filter_today(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter today's registrations.
        """

        if value:
            return queryset.today()

        return queryset

    def filter_this_week(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter this week's registrations.
        """

        if value:
            return queryset.this_week()

        return queryset

    def filter_this_month(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter this month's registrations.
        """

        if value:
            return queryset.this_month()

        return queryset

    def filter_active(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter active registrations.
        """

        if value:
            return queryset.active()

        return queryset

    def filter_needs_verification(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter registrations requiring verification.
        """

        if value:
            return queryset.needs_verification()

        return queryset

    def filter_ready_for_checkin(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter registrations ready for check-in.
        """

        if value:
            return queryset.ready_for_checkin()

        return queryset

    def filter_ready_for_completion(
        self,
        queryset,
        name,
        value,
    ):
        """
        Filter registrations ready for completion.
        """

        if value:
            return queryset.ready_for_completion()

        return queryset
