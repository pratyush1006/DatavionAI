"""
Tests for shared base models.
"""

from __future__ import annotations

from django.test import SimpleTestCase

from apps.core.models import (
    BaseModel,
    TimeStampedModel,
)


class TimeStampedModelTests(SimpleTestCase):
    """
    Tests for TimeStampedModel.
    """

    def test_model_is_abstract(
        self,
    ) -> None:
        self.assertTrue(
            TimeStampedModel._meta.abstract,
        )

    def test_has_created_at_field(
        self,
    ) -> None:
        field_names = {field.name for field in TimeStampedModel._meta.local_fields}

        self.assertIn(
            "created_at",
            field_names,
        )

    def test_has_updated_at_field(
        self,
    ) -> None:
        field_names = {field.name for field in TimeStampedModel._meta.local_fields}

        self.assertIn(
            "updated_at",
            field_names,
        )


class BaseModelTests(SimpleTestCase):
    """
    Tests for BaseModel.
    """

    def test_model_is_abstract(
        self,
    ) -> None:
        self.assertTrue(
            BaseModel._meta.abstract,
        )

    def test_has_uuid_id_field(
        self,
    ) -> None:
        field_names = {field.name for field in BaseModel._meta.local_fields}

        self.assertIn(
            "id",
            field_names,
        )

    def test_has_is_active_field(
        self,
    ) -> None:
        field_names = {field.name for field in BaseModel._meta.local_fields}

        self.assertIn(
            "is_active",
            field_names,
        )
