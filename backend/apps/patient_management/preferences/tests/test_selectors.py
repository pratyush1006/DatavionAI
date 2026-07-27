"""
Selector tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.constants import (
    CommunicationChannel,
)
from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.patient_management.preferences.selectors import (
    get_communication_preference,
    get_communication_preferences,
    get_enabled_communication_preferences,
    get_patient_preference,
    get_patient_preferences,
)
from apps.patient_management.preferences.tests.factories import (
    OrganizationFactory,
    PatientCommunicationPreferenceFactory,
    PatientFactory,
    PatientPreferenceFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceSelectors:
    """
    Tests for PatientPreference selectors.
    """

    def test_get_patient_preferences(
        self,
    ) -> None:
        PatientPreferenceFactory.create_batch(
            5,
        )

        queryset = get_patient_preferences()

        assert queryset.count() == 5

    def test_get_patient_preference(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        preference = PatientPreferenceFactory(
            organization=organization,
            patient=patient,
        )

        result = get_patient_preference(
            organization_id=organization.id,
            patient_id=patient.id,
        )

        assert result == preference

    def test_get_patient_preference_not_found(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        with pytest.raises(
            PatientPreference.DoesNotExist,
        ):
            get_patient_preference(
                organization_id=organization.id,
                patient_id=patient.id,
            )

    def test_get_patient_preference_tenant_isolation(
        self,
    ) -> None:
        organization_one = OrganizationFactory()

        organization_two = OrganizationFactory()

        patient = PatientFactory(
            organization=organization_one,
        )

        PatientPreferenceFactory(
            organization=organization_one,
            patient=patient,
        )

        with pytest.raises(
            PatientPreference.DoesNotExist,
        ):
            get_patient_preference(
                organization_id=organization_two.id,
                patient_id=patient.id,
            )

    def test_get_patient_preferences_select_related(
        self,
    ) -> None:
        PatientPreferenceFactory()

        queryset = get_patient_preferences()

        assert "patient" in queryset.query.select_related
        assert "organization" in queryset.query.select_related


class TestPatientCommunicationPreferenceSelectors:
    """
    Tests for PatientCommunicationPreference selectors.
    """

    def test_get_communication_preferences(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        PatientCommunicationPreferenceFactory.create_batch(
            3,
            organization=organization,
            patient=patient,
        )

        queryset = get_communication_preferences(
            organization_id=organization.id,
            patient_id=patient.id,
        )

        assert queryset.count() == 3

    def test_get_enabled_communication_preferences(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            enabled=True,
            channel=CommunicationChannel.EMAIL,
        )

        PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            enabled=False,
            channel=CommunicationChannel.SMS,
        )

        queryset = get_enabled_communication_preferences(
            organization_id=organization.id,
            patient_id=patient.id,
        )

        assert queryset.count() == 1
        assert queryset.first().enabled is True

    def test_get_communication_preference(
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
        )

        result = get_communication_preference(
            organization_id=organization.id,
            patient_id=patient.id,
            channel=CommunicationChannel.EMAIL,
        )

        assert result == preference

    def test_get_communication_preference_not_found(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        with pytest.raises(
            PatientCommunicationPreference.DoesNotExist,
        ):
            get_communication_preference(
                organization_id=organization.id,
                patient_id=patient.id,
                channel=CommunicationChannel.EMAIL,
            )

    def test_get_communication_preference_tenant_isolation(
        self,
    ) -> None:
        organization_one = OrganizationFactory()

        organization_two = OrganizationFactory()

        patient = PatientFactory(
            organization=organization_one,
        )

        PatientCommunicationPreferenceFactory(
            organization=organization_one,
            patient=patient,
            channel=CommunicationChannel.EMAIL,
        )

        with pytest.raises(
            PatientCommunicationPreference.DoesNotExist,
        ):
            get_communication_preference(
                organization_id=organization_two.id,
                patient_id=patient.id,
                channel=CommunicationChannel.EMAIL,
            )

    def test_get_communication_preferences_are_ordered(
        self,
    ) -> None:
        organization = OrganizationFactory()

        patient = PatientFactory(
            organization=organization,
        )

        first = PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            priority=1,
            channel=CommunicationChannel.EMAIL,
        )

        second = PatientCommunicationPreferenceFactory(
            organization=organization,
            patient=patient,
            priority=2,
            channel=CommunicationChannel.SMS,
        )

        queryset = get_communication_preferences(
            organization_id=organization.id,
            patient_id=patient.id,
        )

        assert list(queryset) == [
            first,
            second,
        ]
