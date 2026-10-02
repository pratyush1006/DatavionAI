from django.test import SimpleTestCase, override_settings

from apps.ai.services.provider_errors import classify_provider_error


class ProviderDeploymentContractTests(SimpleTestCase):
    def test_insufficient_quota_is_not_retryable(self):
        result = classify_provider_error(
            status_code=429,
            code="credit_balance_exhausted",
            error_type="insufficient_quota",
        )
        self.assertTrue(result.quota_exhausted)
        self.assertFalse(result.retryable)

    def test_transient_429_is_retryable(self):
        result = classify_provider_error(
            status_code=429,
            code="rate_limit_exceeded",
            error_type="rate_limit_error",
        )
        self.assertFalse(result.quota_exhausted)
        self.assertTrue(result.retryable)

    @override_settings(OPENAI_API_KEY="configured-secret")
    def test_provider_reads_central_django_setting(self):
        from apps.ai.providers.implementation.openai import OpenAIProvider

        provider = OpenAIProvider()
        self.assertEqual(provider.api_key, "configured-secret")
