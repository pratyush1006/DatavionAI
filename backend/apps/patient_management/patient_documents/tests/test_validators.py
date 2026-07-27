"""
Tests for Patient Document validators.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.patient_management.patient_documents.validators import (
    validate_document_size,
)


class DummyFile:
    """
    Dummy uploaded file.
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.content_type = "application/pdf"


class PatientDocumentValidatorTestCase(TestCase):
    """
    Tests for document validators.
    """

    def test_validate_document_size_success(self) -> None:
        """
        Small files should pass validation.
        """

        file = DummyFile(
            size=1024,
        )

        validate_document_size(
            file,
        )

    def test_validate_document_size_failure(self) -> None:
        """
        Large files should fail validation.
        """

        file = DummyFile(
            size=100 * 1024 * 1024,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_document_size(
                file,
            )
