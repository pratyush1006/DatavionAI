from django.test import SimpleTestCase

from apps.common.models import BaseModel, TimeStampedModel


class TimeStampedModelTests(SimpleTestCase):
    """Tests for TimeStampedModel."""

    def test_model_is_abstract(self):
        self.assertTrue(TimeStampedModel._meta.abstract)

    def test_has_created_at_field(self):
        self.assertIn(
            "created_at", [field.name for field in TimeStampedModel._meta.local_fields]
        )

    def test_has_updated_at_field(self):
        self.assertIn(
            "updated_at", [field.name for field in TimeStampedModel._meta.local_fields]
        )


class BaseModelTests(SimpleTestCase):
    """Tests for BaseModel."""

    def test_model_is_abstract(self):
        self.assertTrue(BaseModel._meta.abstract)

    def test_has_uuid_id_field(self):
        self.assertIn("id", [field.name for field in BaseModel._meta.local_fields])

    def test_has_is_active_field(self):
        self.assertIn(
            "is_active", [field.name for field in BaseModel._meta.local_fields]
        )
