"""
Model tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.patient_management.preferences.constants import (
    CommunicationChannel,
    PreferenceStatus,
)
from apps.patient_management.preferences.tests.factories import (
    PatientCommunicationPreferenceFactory,
    PatientPreferenceFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceModel:
    """
    Tests for PatientPreference.
    """

    def test_create_patient_preference(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.pk is not None
        assert preference.uuid is not None

    def test_default_status(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.status == PreferenceStatus.ACTIVE

    def test_has_patient(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.patient is not None

    def test_has_organization(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.organization is not None

    def test_string_representation(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert str(preference)

    def test_full_clean(
        self,
    ) -> None:
        preference = PatientPreferenceFactory.build()

        preference.full_clean()

    def test_unique_patient_constraint(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        with pytest.raises(
            IntegrityError,
        ):
            PatientPreferenceFactory(
                organization=preference.organization,
                patient=preference.patient,
            )

    def test_uuid_generated(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.uuid is not None

    def test_created_timestamp(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.created_at is not None

    def test_updated_timestamp(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        assert preference.updated_at is not None


class TestPatientCommunicationPreferenceModel:
    """
    Tests for PatientCommunicationPreference.
    """

    def test_create(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.pk is not None

    def test_default_enabled(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.enabled is True

    def test_default_channel(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.channel == CommunicationChannel.EMAIL

    def test_string_representation(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert str(preference)

    def test_full_clean(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory.build()

        preference.full_clean()

    def test_unique_channel_constraint(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        with pytest.raises(
            IntegrityError,
        ):
            PatientCommunicationPreferenceFactory(
                organization=preference.organization,
                patient=preference.patient,
                channel=preference.channel,
            )

    def test_uuid_generated(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.uuid is not None

    def test_created_timestamp(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.created_at is not None

    def test_updated_timestamp(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        assert preference.updated_at is not None

    def test_invalid_priority(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory.build(
            priority=-1,
        )

        with pytest.raises(
            ValidationError,
        ):
            preference.full_clean()
