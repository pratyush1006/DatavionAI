from django.test import SimpleTestCase

from apps.common.storage.registry import (
    StorageRegistry,
)


class TestStorageRegistry(
    SimpleTestCase,
):
    def test_backend_registration_and_lookup(
        self,
    ):
        registry = StorageRegistry()

        class DummyBackend:
            def upload(
                self,
                path,
                content,
                *,
                overwrite=False,
            ):
                return None

            def download(
                self,
                path,
            ):
                return b""

            def delete(
                self,
                path,
            ):
                return True

            def exists(
                self,
                path,
            ):
                return True

            def get_url(
                self,
                path,
                *,
                expires_in=None,
            ):
                return "url"

            def size(
                self,
                path,
            ):
                return 0

        backend = DummyBackend()

        registry.register_backend(
            backend,
        )

        result = registry.get_backend(
            "DummyBackend",
        )

        self.assertEqual(
            result,
            backend,
        )
