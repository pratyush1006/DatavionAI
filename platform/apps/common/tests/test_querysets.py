from django.test import SimpleTestCase

from apps.common.models import BaseQuerySet


class BaseQuerySetTests(SimpleTestCase):
    """Tests for BaseQuerySet."""

    def test_has_active_method(self):
        self.assertTrue(hasattr(BaseQuerySet, "active"))

    def test_has_inactive_method(self):
        self.assertTrue(hasattr(BaseQuerySet, "inactive"))

    def test_has_ordered_method(self):
        self.assertTrue(hasattr(BaseQuerySet, "ordered"))
