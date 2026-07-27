"""
Serializer tests for the Patient Preferences module.
"""

from __future__ import annotations

import pytest

from apps.patient_management.preferences.api.serializers import (
    PatientCommunicationPreferenceCreateSerializer,
    PatientCommunicationPreferenceDetailSerializer,
    PatientCommunicationPreferenceListSerializer,
    PatientCommunicationPreferenceUpdateSerializer,
    PatientPreferenceCreateSerializer,
    PatientPreferenceDetailSerializer,
    PatientPreferenceListSerializer,
    PatientPreferenceUpdateSerializer,
)
from apps.patient_management.preferences.constants import (
    CommunicationChannel,
    PreferenceStatus,
)
from apps.patient_management.preferences.tests.factories import (
    PatientCommunicationPreferenceFactory,
    PatientPreferenceFactory,
)

pytestmark = pytest.mark.django_db


class TestPatientPreferenceCreateSerializer:
    """
    Tests for PatientPreferenceCreateSerializer.
    """

    def test_valid_serializer(
        self,
    ) -> None:
        instance = PatientPreferenceFactory.build()

        serializer = PatientPreferenceCreateSerializer(
            data={
                "organization": instance.organization.pk,
                "patient": instance.patient.pk,
                "language": instance.language,
                "timezone": instance.timezone,
                "preferred_name": instance.preferred_name,
                "portal_theme": instance.portal_theme,
                "appointment_reminder": instance.appointment_reminder,
                "accessibility_mode": instance.accessibility_mode,
                "ai_personalization": instance.ai_personalization,
                "data_sharing_consent": instance.data_sharing_consent,
                "status": instance.status,
            },
        )

        assert serializer.is_valid(), serializer.errors

    def test_invalid_serializer(
        self,
    ) -> None:
        serializer = PatientPreferenceCreateSerializer(
            data={},
        )

        assert not serializer.is_valid()


class TestPatientPreferenceUpdateSerializer:
    """
    Tests for PatientPreferenceUpdateSerializer.
    """

    def test_update_serializer(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        serializer = PatientPreferenceUpdateSerializer(
            preference,
            data={
                "preferred_name": "Updated",
                "status": PreferenceStatus.INACTIVE,
            },
            partial=True,
        )

        assert serializer.is_valid(), serializer.errors

        instance = serializer.save()

        assert instance.preferred_name == "Updated"
        assert instance.status == PreferenceStatus.INACTIVE


class TestPatientPreferenceListSerializer:
    """
    Tests for PatientPreferenceListSerializer.
    """

    def test_serialized_fields(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        serializer = PatientPreferenceListSerializer(
            preference,
        )

        assert serializer.data["uuid"]
        assert serializer.data["patient"]


class TestPatientPreferenceDetailSerializer:
    """
    Tests for PatientPreferenceDetailSerializer.
    """

    def test_detail_serializer(
        self,
    ) -> None:
        preference = PatientPreferenceFactory()

        serializer = PatientPreferenceDetailSerializer(
            preference,
        )

        assert serializer.data["uuid"]


class TestCommunicationPreferenceCreateSerializer:
    """
    Tests for PatientCommunicationPreferenceCreateSerializer.
    """

    def test_valid_serializer(
        self,
    ) -> None:
        instance = PatientCommunicationPreferenceFactory.build()

        serializer = PatientCommunicationPreferenceCreateSerializer(
            data={
                "organization": instance.organization.pk,
                "patient": instance.patient.pk,
                "channel": instance.channel,
                "priority": instance.priority,
                "enabled": instance.enabled,
                "appointment_notifications": (instance.appointment_notifications),
                "clinical_notifications": (instance.clinical_notifications),
                "laboratory_notifications": (instance.laboratory_notifications),
                "radiology_notifications": (instance.radiology_notifications),
                "pharmacy_notifications": (instance.pharmacy_notifications),
                "billing_notifications": (instance.billing_notifications),
                "insurance_notifications": (instance.insurance_notifications),
                "marketing_notifications": (instance.marketing_notifications),
                "emergency_notifications": (instance.emergency_notifications),
                "ai_assistant_notifications": (instance.ai_assistant_notifications),
            },
        )

        assert serializer.is_valid(), serializer.errors

    def test_invalid_channel(
        self,
    ) -> None:
        instance = PatientCommunicationPreferenceFactory.build()

        serializer = PatientCommunicationPreferenceCreateSerializer(
            data={
                "organization": instance.organization.pk,
                "patient": instance.patient.pk,
                "channel": "INVALID",
            },
        )

        assert not serializer.is_valid()


class TestCommunicationPreferenceUpdateSerializer:
    """
    Tests for PatientCommunicationPreferenceUpdateSerializer.
    """

    def test_update_serializer(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        serializer = PatientCommunicationPreferenceUpdateSerializer(
            preference,
            data={
                "enabled": False,
                "channel": CommunicationChannel.SMS,
            },
            partial=True,
        )

        assert serializer.is_valid(), serializer.errors

        instance = serializer.save()

        assert instance.enabled is False
        assert instance.channel == CommunicationChannel.SMS


class TestCommunicationPreferenceListSerializer:
    """
    Tests for PatientCommunicationPreferenceListSerializer.
    """

    def test_list_serializer(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        serializer = PatientCommunicationPreferenceListSerializer(
            preference,
        )

        assert serializer.data["uuid"]
        assert serializer.data["channel"]


class TestCommunicationPreferenceDetailSerializer:
    """
    Tests for PatientCommunicationPreferenceDetailSerializer.
    """

    def test_detail_serializer(
        self,
    ) -> None:
        preference = PatientCommunicationPreferenceFactory()

        serializer = PatientCommunicationPreferenceDetailSerializer(
            preference,
        )

        assert serializer.data["uuid"]
