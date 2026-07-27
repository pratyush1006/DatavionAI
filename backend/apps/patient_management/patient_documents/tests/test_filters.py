"""
Tests for Patient Document filters.
"""

from __future__ import annotations

from django.test import TestCase

from apps.organizations.tests.factories import (
    create_organization,
)
from apps.patient_management.patient_documents.api.filters import (
    PatientDocumentFilter,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patients.tests.factories import (
    create_patient,
)

from .factories import (
    create_patient_document,
)


class PatientDocumentFilterTestCase(TestCase):
    """
    Tests for Patient Document filters.
    """

    def setUp(self) -> None:
        self.organization = create_organization()

        self.patient = create_patient(
            organization=self.organization,
        )

        create_patient_document(
            organization=self.organization,
            patient=self.patient,
        )

    def test_filter_by_category(self) -> None:
        queryset = PatientDocument.objects.all()

        filtered = PatientDocumentFilter(
            {
                "category": "LABORATORY",
            },
            queryset=queryset,
        )

        self.assertEqual(
            filtered.qs.count(),
            1,
        )
