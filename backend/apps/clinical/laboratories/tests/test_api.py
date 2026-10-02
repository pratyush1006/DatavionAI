from django.test import SimpleTestCase

from apps.clinical.laboratories.urls import urlpatterns


class LaboratoryAPITests(SimpleTestCase):
    def test_router_contains_all_major_resources(self):
        self.assertGreaterEqual(len(urlpatterns), 7)
