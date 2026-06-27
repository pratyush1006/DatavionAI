from django.test import SimpleTestCase

from apps.common.models import BaseManager


class BaseManagerTests(SimpleTestCase):
    """Tests for BaseManager."""

    def test_has_active_method(self):
        self.assertTrue(hasattr(BaseManager, "active"))

    def test_has_inactive_method(self):
        self.assertTrue(hasattr(BaseManager, "inactive"))

    def test_has_ordered_method(self):
        self.assertTrue(hasattr(BaseManager, "ordered"))
