"""Generated Provider model contract tests for forward repair."""

from django.test import SimpleTestCase


class ProviderModelContractTests(SimpleTestCase):
    def test_provider_model_contract(self):
        from apps.clinical.providers.models import Provider

        field_names = {field.name for field in Provider._meta.get_fields()}
        self.assertNotIn("license_number", field_names)
        for required in {
            "organization",
            "employee",
            "provider_number",
            "provider_type",
            "status",
        }:
            self.assertIn(required, field_names)
