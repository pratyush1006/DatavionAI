"""
Signal tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.patient_management.preferences.tests.factories import (
    PatientFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceSignals:
    """
    Tests for PatientPreference signals.
    """

    def test_patient_creation_creates_preference(
        self,
    ) -> None:
        """
        A PatientPreference should automatically be
        created when a patient is created.
        """
        patient = PatientFactory()

        preference = PatientPreference.objects.get(
            organization=patient.organization,
            patient=patient,
        )

        assert preference.patient == patient
        assert preference.organization == patient.organization

    def test_patient_preference_created_once(
        self,
    ) -> None:
        """
        Saving an existing patient should not create
        duplicate preferences.
        """
        patient = PatientFactory()

        patient.first_name = "Updated"

        patient.save()

        assert (
            PatientPreference.objects.filter(
                organization=patient.organization,
                patient=patient,
            ).count()
            == 1
        )

    def test_preference_belongs_to_patient_organization(
        self,
    ) -> None:
        """
        Preference should belong to the patient's
        organization.
        """
        patient = PatientFactory()

        preference = PatientPreference.objects.get(
            patient=patient,
        )

        assert preference.organization == patient.organization

    def test_multiple_patients_have_independent_preferences(
        self,
    ) -> None:
        """
        Each patient should receive an independent
        preference record.
        """
        patient_one = PatientFactory()

        patient_two = PatientFactory()

        assert (
            PatientPreference.objects.filter(
                patient=patient_one,
            ).count()
            == 1
        )

        assert (
            PatientPreference.objects.filter(
                patient=patient_two,
            ).count()
            == 1
        )


class TestPatientCommunicationPreferenceSignals:
    """
    Tests for communication preference signals.
    """

    def test_no_communication_preferences_created_by_default(
        self,
    ) -> None:
        """
        Communication preferences are not created
        automatically.
        """
        patient = PatientFactory()

        assert (
            PatientCommunicationPreference.objects.filter(
                patient=patient,
            ).count()
            == 0
        )

    @pytest.mark.skip(
        reason=(
            "Enable after automatic communication preference creation is implemented."
        ),
    )
    def test_default_communication_preferences_created(
        self,
    ) -> None:
        """
        Future behavior:
        Default communication preferences should be
        created when a patient is created.
        """
        patient = PatientFactory()

        assert PatientCommunicationPreference.objects.filter(
            patient=patient,
        ).exists()

    @pytest.mark.skip(
        reason=(
            "Enable after automatic communication preference creation is implemented."
        ),
    )
    def test_default_channels_created(
        self,
    ) -> None:
        """
        Future behavior:
        Verify all default communication channels
        are created.
        """
        patient = PatientFactory()

        queryset = PatientCommunicationPreference.objects.filter(
            patient=patient,
        )

        assert queryset.count() == 5

    @pytest.mark.skip(
        reason=(
            "Enable after automatic communication preference creation is implemented."
        ),
    )
    def test_default_priorities(
        self,
    ) -> None:
        """
        Future behavior:
        Verify channel priorities.
        """
        patient = PatientFactory()

        queryset = PatientCommunicationPreference.objects.filter(
            patient=patient,
        ).order_by(
            "priority",
        )

        priorities = list(
            queryset.values_list(
                "priority",
                flat=True,
            )
        )

        assert priorities == [
            1,
            2,
            3,
            4,
            5,
        ]
