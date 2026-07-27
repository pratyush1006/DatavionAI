"""
Filter tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.api.filters import (
    PatientCommunicationPreferenceFilter,
    PatientPreferenceFilter,
)
from apps.patient_management.preferences.constants import (
    CommunicationChannel,
    PreferenceStatus,
)
from apps.patient_management.preferences.tests.factories import (
    OrganizationFactory,
    PatientCommunicationPreferenceFactory,
    PatientFactory,
    PatientPreferenceFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceFilter:
    """
    Tests for PatientPreferenceFilter.
    """

    def test_filter_by_organization(
        self,
    ) -> None:
        organization = OrganizationFactory()

        PatientPreferenceFactory.create_batch(
            3,
            organization=organization,
        )

        PatientPreferenceFactory()

        queryset = PatientPreferenceFilter(
            data={
                "organization": organization.uuid,
            },
        ).qs

        assert queryset.count() == 3

    def test_filter_by_patient(
        self,
    ) -> None:
        patient = PatientFactory()

        PatientPreferenceFactory(
            organization=patient.organization,
            patient=patient,
        )

        PatientPreferenceFactory()

        queryset = PatientPreferenceFilter(
            data={
                "patient": patient.uuid,
            },
        ).qs

        assert queryset.count() == 1

    def test_filter_by_language(
        self,
    ) -> None:
        PatientPreferenceFactory(
            language="en",
        )

        PatientPreferenceFactory(
            language="fr",
        )

        queryset = PatientPreferenceFilter(
            data={
                "language": "en",
            },
        ).qs

        assert queryset.count() == 1

    def test_filter_by_status(
        self,
    ) -> None:
        PatientPreferenceFactory(
            status=PreferenceStatus.ACTIVE,
        )

        PatientPreferenceFactory(
            status=PreferenceStatus.INACTIVE,
        )

        queryset = PatientPreferenceFilter(
            data={
                "status": PreferenceStatus.ACTIVE,
            },
        ).qs

        assert queryset.count() == 1

    def test_empty_filter_returns_all(
        self,
    ) -> None:
        PatientPreferenceFactory.create_batch(
            5,
        )

        queryset = PatientPreferenceFilter().qs

        assert queryset.count() == 5


class TestPatientCommunicationPreferenceFilter:
    """
    Tests for PatientCommunicationPreferenceFilter.
    """

    def test_filter_by_patient(
        self,
    ) -> None:
        patient = PatientFactory()

        PatientCommunicationPreferenceFactory(
            organization=patient.organization,
            patient=patient,
        )

        PatientCommunicationPreferenceFactory()

        queryset = PatientCommunicationPreferenceFilter(
            data={
                "patient": patient.uuid,
            },
        ).qs

        assert queryset.count() == 1

    def test_filter_by_organization(
        self,
    ) -> None:
        organization = OrganizationFactory()

        PatientCommunicationPreferenceFactory.create_batch(
            4,
            organization=organization,
        )

        PatientCommunicationPreferenceFactory()

        queryset = PatientCommunicationPreferenceFilter(
            data={
                "organization": organization.uuid,
            },
        ).qs

        assert queryset.count() == 4

    def test_filter_by_channel(
        self,
    ) -> None:
        PatientCommunicationPreferenceFactory(
            channel=CommunicationChannel.EMAIL,
        )

        PatientCommunicationPreferenceFactory(
            channel=CommunicationChannel.SMS,
        )

        queryset = PatientCommunicationPreferenceFilter(
            data={
                "channel": CommunicationChannel.EMAIL,
            },
        ).qs

        assert queryset.count() == 1

    def test_filter_by_enabled(
        self,
    ) -> None:
        PatientCommunicationPreferenceFactory(
            enabled=True,
        )

        PatientCommunicationPreferenceFactory(
            enabled=False,
        )

        queryset = PatientCommunicationPreferenceFilter(
            data={
                "enabled": True,
            },
        ).qs

        assert queryset.count() == 1

    def test_multiple_filters(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            channel=CommunicationChannel.EMAIL,
            enabled=True,
        )

        PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            channel=CommunicationChannel.SMS,
            enabled=False,
        )

        queryset = PatientCommunicationPreferenceFilter(
            data={
                "organization": organization.uuid,
                "patient": patient.uuid,
                "channel": CommunicationChannel.EMAIL,
                "enabled": True,
            },
        ).qs

        assert queryset.count() == 1

    def test_empty_filter_returns_all(
        self,
    ) -> None:
        PatientCommunicationPreferenceFactory.create_batch(
            5,
        )

        queryset = PatientCommunicationPreferenceFilter().qs

        assert queryset.count() == 5
