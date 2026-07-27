"""
Manager and QuerySet tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

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


class TestPatientPreferenceQuerySet:
    """
    Tests for PatientPreferenceQuerySet.
    """

    def test_active(
        self,
    ) -> None:
        active = PatientPreferenceFactory(
            status=PreferenceStatus.ACTIVE,
        )

        PatientPreferenceFactory(
            status=PreferenceStatus.INACTIVE,
        )

        queryset = active.__class__.objects.active()

        assert queryset.count() == 1
        assert active in queryset

    def test_inactive(
        self,
    ) -> None:
        inactive = PatientPreferenceFactory(
            status=PreferenceStatus.INACTIVE,
        )

        PatientPreferenceFactory(
            status=PreferenceStatus.ACTIVE,
        )

        queryset = inactive.__class__.objects.inactive()

        assert queryset.count() == 1
        assert inactive in queryset

    def test_by_organization(
        self,
    ) -> None:
        organization = OrganizationFactory()

        preference = PatientPreferenceFactory(
            organization=organization,
        )

        PatientPreferenceFactory()

        queryset = preference.__class__.objects.by_organization(
            organization.id,
        )

        assert queryset.count() == 1
        assert preference in queryset

    def test_by_patient(
        self,
    ) -> None:
        patient = PatientFactory()

        preference = PatientPreferenceFactory(
            patient=patient,
            organization=patient.organization,
        )

        PatientPreferenceFactory()

        queryset = preference.__class__.objects.by_patient(
            patient.id,
        )

        assert queryset.count() == 1
        assert preference in queryset

    def test_chain_queryset(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        preference = PatientPreferenceFactory(
            organization=organization,
            patient=patient,
            status=PreferenceStatus.ACTIVE,
        )

        PatientPreferenceFactory(
            organization=organization,
            status=PreferenceStatus.INACTIVE,
        )

        queryset = (
            preference.__class__.objects.active()
            .by_organization(
                organization.id,
            )
            .by_patient(
                patient.id,
            )
        )

        assert queryset.count() == 1
        assert queryset.first() == preference


class TestPatientCommunicationPreferenceQuerySet:
    """
    Tests for PatientCommunicationPreferenceQuerySet.
    """

    def test_enabled(
        self,
    ) -> None:
        enabled = PatientCommunicationPreferenceFactory(
            enabled=True,
        )

        PatientCommunicationPreferenceFactory(
            enabled=False,
        )

        queryset = enabled.__class__.objects.enabled()

        assert queryset.count() == 1
        assert enabled in queryset

    def test_disabled(
        self,
    ) -> None:
        disabled = PatientCommunicationPreferenceFactory(
            enabled=False,
        )

        PatientCommunicationPreferenceFactory(
            enabled=True,
        )

        queryset = disabled.__class__.objects.disabled()

        assert queryset.count() == 1
        assert disabled in queryset

    def test_by_organization(
        self,
    ) -> None:
        organization = OrganizationFactory()

        preference = PatientCommunicationPreferenceFactory(
            organization=organization,
        )

        PatientCommunicationPreferenceFactory()

        queryset = preference.__class__.objects.by_organization(
            organization.id,
        )

        assert queryset.count() == 1
        assert preference in queryset

    def test_by_patient(
        self,
    ) -> None:
        patient = PatientFactory()

        preference = PatientCommunicationPreferenceFactory(
            organization=patient.organization,
            patient=patient,
        )

        PatientCommunicationPreferenceFactory()

        queryset = preference.__class__.objects.by_patient(
            patient.id,
        )

        assert queryset.count() == 1
        assert preference in queryset

    def test_by_channel(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory(
            channel=CommunicationChannel.EMAIL,
        )

        PatientCommunicationPreferenceFactory(
            channel=CommunicationChannel.SMS,
        )

        queryset = preference.__class__.objects.by_channel(
            CommunicationChannel.EMAIL,
        )

        assert queryset.count() == 1
        assert preference in queryset

    def test_ordered(
        self,
    ) -> None:
        low = PatientCommunicationPreferenceFactory(
            priority=1,
        )

        high = PatientCommunicationPreferenceFactory(
            priority=10,
            channel=CommunicationChannel.SMS,
        )

        queryset = low.__class__.objects.ordered()

        assert list(queryset[:2]) == [
            low,
            high,
        ]

    def test_chain_queryset(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        preference = PatientCommunicationPreferenceFactory(
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

        queryset = (
            preference.__class__.objects.enabled()
            .by_organization(
                organization.id,
            )
            .by_patient(
                patient.id,
            )
            .by_channel(
                CommunicationChannel.EMAIL,
            )
        )

        assert queryset.count() == 1
        assert queryset.first() == preference
