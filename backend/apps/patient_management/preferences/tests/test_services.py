"""
Service tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.constants import (
    CommunicationChannel,
    PreferenceStatus,
)
from apps.patient_management.preferences.models import (
    PatientCommunicationPreference,
    PatientPreference,
)
from apps.patient_management.preferences.services import (
    create_communication_preference,
    create_patient_preference,
    delete_communication_preference,
    delete_patient_preference,
    update_communication_preference,
    update_patient_preference,
)
from apps.patient_management.preferences.tests.factories import (
    PatientCommunicationPreferenceFactory,
    PatientPreferenceFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceServices:
    """
    Tests for PatientPreference services.
    """

    def test_create_patient_preference(
        self,
    ) -> None:
        template = PatientPreferenceFactory.build()

        preference = create_patient_preference(
            organization=template.organization,
            patient=template.patient,
            language=template.language,
            timezone=template.timezone,
            preferred_name=template.preferred_name,
            portal_theme=template.portal_theme,
            appointment_reminder=template.appointment_reminder,
            accessibility_mode=template.accessibility_mode,
            ai_personalization=template.ai_personalization,
            data_sharing_consent=template.data_sharing_consent,
            status=template.status,
        )

        assert isinstance(
            preference,
            PatientPreference,
        )

        assert PatientPreference.objects.filter(
            pk=preference.pk,
        ).exists()

    def test_update_patient_preference(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        update_patient_preference(
            preference=preference,
            preferred_name="John",
            status=PreferenceStatus.INACTIVE,
        )

        preference.refresh_from_db()

        assert preference.preferred_name == "John"
        assert preference.status == PreferenceStatus.INACTIVE

    def test_delete_patient_preference(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        pk = preference.pk

        delete_patient_preference(
            preference=preference,
        )

        assert not PatientPreference.objects.filter(
            pk=pk,
        ).exists()

    def test_partial_update(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        language = preference.language

        update_patient_preference(
            preference=preference,
            preferred_name="Updated",
        )

        preference.refresh_from_db()

        assert preference.preferred_name == "Updated"

        assert preference.language == language


class TestPatientCommunicationPreferenceServices:
    """
    Tests for PatientCommunicationPreference services.
    """

    def test_create_communication_preference(
        self,
    ) -> None:
        template = PatientCommunicationPreferenceFactory.build()

        preference = create_communication_preference(
            organization=template.organization,
            patient=template.patient,
            channel=template.channel,
            priority=template.priority,
            enabled=template.enabled,
            appointment_notifications=(template.appointment_notifications),
            clinical_notifications=(template.clinical_notifications),
            laboratory_notifications=(template.laboratory_notifications),
            radiology_notifications=(template.radiology_notifications),
            pharmacy_notifications=(template.pharmacy_notifications),
            billing_notifications=(template.billing_notifications),
            insurance_notifications=(template.insurance_notifications),
            marketing_notifications=(template.marketing_notifications),
            emergency_notifications=(template.emergency_notifications),
            ai_assistant_notifications=(template.ai_assistant_notifications),
        )

        assert isinstance(
            preference,
            PatientCommunicationPreference,
        )

    def test_update_communication_preference(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        update_communication_preference(
            preference=preference,
            enabled=False,
            priority=5,
        )

        preference.refresh_from_db()

        assert preference.enabled is False
        assert preference.priority == 5

    def test_delete_communication_preference(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        pk = preference.pk

        delete_communication_preference(
            preference=preference,
        )

        assert not PatientCommunicationPreference.objects.filter(
            pk=pk,
        ).exists()

    def test_update_channel(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        update_communication_preference(
            preference=preference,
            channel=CommunicationChannel.SMS,
        )

        preference.refresh_from_db()

        assert preference.channel == CommunicationChannel.SMS

    def test_partial_update(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        priority = preference.priority

        update_communication_preference(
            preference=preference,
            enabled=False,
        )

        preference.refresh_from_db()

        assert preference.enabled is False
        assert preference.priority == priority
