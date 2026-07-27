"""
Tests for patient serializers.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

from apps.clinical.patients.api.serializers import (
    PatientBaseSerializer,
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientListSerializer,
    PatientUpdateSerializer,
)
from apps.clinical.patients.constants import PatientGender
from apps.clinical.patients.tests.factories import PatientFactory
from apps.common.tests.base import BaseTestCase


class PatientSerializerTestCase(BaseTestCase):
    """
    Test cases for patient serializers.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(
                1995,
                5,
                20,
            ),
            gender=PatientGender.MALE,
        )

    def test_base_serializer_normalizes_mrn(self) -> None:
        """
        MRN should be normalized.
        """

        serializer = PatientBaseSerializer()

        self.assertEqual(
            serializer.validate_mrn(
                "  mrn000123  ",
            ),
            "MRN000123",
        )

    def test_base_serializer_normalizes_email(self) -> None:
        """
        Email should be normalized.
        """

        serializer = PatientBaseSerializer()

        self.assertEqual(
            serializer.validate_email(
                "  TEST@Example.COM ",
            ),
            "test@example.com",
        )

    def test_base_serializer_normalizes_first_name(self) -> None:
        """
        First name should be trimmed.
        """

        serializer = PatientBaseSerializer()

        self.assertEqual(
            serializer.validate_first_name(
                "  John  ",
            ),
            "John",
        )

    @patch(
        "apps.clinical.patients.api.serializers.create.PatientService.create",
    )
    def test_create_serializer_delegates_to_service(
        self,
        mock_create,
    ) -> None:
        """
        Create serializer should delegate to PatientService.
        """

        mock_create.return_value = self.patient

        serializer = PatientCreateSerializer()

        patient = serializer.create(
            {
                "organization": self.organization,
                "mrn": "MRN000002",
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": date(
                    1998,
                    1,
                    1,
                ),
                "gender": PatientGender.FEMALE,
            },
        )

        self.assertEqual(
            patient,
            self.patient,
        )

        mock_create.assert_called_once()

    @patch(
        "apps.clinical.patients.api.serializers.update.PatientService.update",
    )
    def test_update_serializer_delegates_to_service(
        self,
        mock_update,
    ) -> None:
        """
        Update serializer should delegate to PatientService.
        """

        mock_update.return_value = self.patient

        serializer = PatientUpdateSerializer()

        patient = serializer.update(
            self.patient,
            {
                "first_name": "Jonathan",
            },
        )

        self.assertEqual(
            patient,
            self.patient,
        )

        mock_update.assert_called_once()

    def test_list_serializer_contains_expected_fields(
        self,
    ) -> None:
        """
        List serializer should expose list fields.
        """

        serializer = PatientListSerializer(
            instance=self.patient,
        )

        self.assertIn(
            "mrn",
            serializer.data,
        )

        self.assertIn(
            "display_name",
            serializer.data,
        )

        self.assertIn(
            "status",
            serializer.data,
        )

    def test_detail_serializer_contains_expected_fields(
        self,
    ) -> None:
        """
        Detail serializer should expose detail fields.
        """

        serializer = PatientDetailSerializer(
            instance=self.patient,
        )

        self.assertIn(
            "first_name",
            serializer.data,
        )

        self.assertIn(
            "last_name",
            serializer.data,
        )

        self.assertIn(
            "display_name",
            serializer.data,
        )

        self.assertIn(
            "age",
            serializer.data,
        )

        self.assertIn(
            "organization",
            serializer.data,
        )

    def test_read_only_fields_are_configured(
        self,
    ) -> None:
        """
        Read-only fields should be configured.
        """

        serializer = PatientCreateSerializer()

        self.assertIn(
            "id",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "display_name",
            serializer.Meta.read_only_fields,
        )

        self.assertIn(
            "age",
            serializer.Meta.read_only_fields,
        )


__all__ = [
    "PatientSerializerTestCase",
]
