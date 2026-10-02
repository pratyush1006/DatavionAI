from django.test import SimpleTestCase

from apps.common.search.exceptions import SearchProviderNotFoundError
from apps.common.search.registry import SEARCH_PROVIDERS, get_search_provider
from apps.common.search.vector.registry import VECTOR_PROVIDERS, get_vector_provider


class SearchProviderReadinessTests(SimpleTestCase):
    def test_noop_search_providers_are_not_registered(self):
        self.assertNotIn("postgres", SEARCH_PROVIDERS)
        self.assertNotIn("vector", SEARCH_PROVIDERS)

    def test_unconfigured_keyword_provider_fails_with_service_unavailable(self):
        with self.assertRaises(SearchProviderNotFoundError) as raised:
            get_search_provider("postgres")

        self.assertEqual(raised.exception.status_code, 503)

    def test_noop_vector_backends_are_not_registered(self):
        self.assertNotIn("pgvector", VECTOR_PROVIDERS)
        self.assertNotIn("pinecone", VECTOR_PROVIDERS)
        self.assertNotIn("chromadb", VECTOR_PROVIDERS)
        self.assertNotIn("faiss", VECTOR_PROVIDERS)
        self.assertNotIn("azure_ai_search", VECTOR_PROVIDERS)

    def test_unconfigured_vector_provider_fails_with_service_unavailable(self):
        with self.assertRaises(SearchProviderNotFoundError) as raised:
            get_vector_provider("pgvector")

        self.assertEqual(raised.exception.status_code, 503)
