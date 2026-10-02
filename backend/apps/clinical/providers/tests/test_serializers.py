"""Generated Provider serializer contract tests for forward repair."""

from django.test import SimpleTestCase


class ProviderSerializerContractTests(SimpleTestCase):
    def test_provider_serializer_module_imports(self):
        import apps.clinical.providers.api.serializers as serializers

        self.assertIsNotNone(serializers)
