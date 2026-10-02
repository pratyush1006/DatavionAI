from pathlib import Path

from django.test import SimpleTestCase


class StorageArchitectureTests(SimpleTestCase):
    def setUp(self):
        self.apps_root = Path(__file__).resolve().parents[2]
        self.storage_root = self.apps_root / "common" / "storage"

    def test_single_document_domain(self):
        self.assertTrue((self.apps_root / "documents").exists())
        self.assertFalse((self.apps_root / "common" / "documents").exists())

    def test_single_storage_infrastructure(self):
        self.assertTrue(self.storage_root.exists())
        self.assertFalse((self.apps_root / "storage").exists())
        self.assertFalse((self.apps_root / "common" / "file_storage").exists())
        self.assertFalse((self.apps_root / "common" / "file_storage_service").exists())

    def test_storage_client_and_backend_contract(self):
        from apps.common.storage.backend import StorageBackend
        from apps.common.storage.client import StorageClient

        self.assertTrue(StorageBackend)
        self.assertTrue(StorageClient)

    def test_configured_storage_client_contract(self):
        from apps.common.storage.config import get_storage_client

        client = get_storage_client()
        self.assertIsNotNone(client)

        for operation in (
            "upload",
            "download",
            "delete",
            "exists",
            "url",
            "size",
        ):
            self.assertTrue(callable(getattr(client, operation, None)))

    def test_legacy_service_is_retired(self):
        self.assertFalse((self.storage_root / "service.py").exists())

    def test_patient_gateway_uses_canonical_storage(self):
        gateway = (
            self.apps_root / "patient_management" / "patient_documents" / "storage.py"
        )
        self.assertTrue(gateway.exists())
        text = gateway.read_text(encoding="utf-8")
        self.assertIn("StorageClient", text)
        self.assertIn("get_storage_client", text)
        self.assertNotIn("apps.common.storage.service", text)

    def test_patient_storage_package_is_retired(self):
        patient = self.apps_root / "patient_management" / "patient_documents"
        self.assertFalse((patient / "storage").exists())

    def test_documents_has_no_competing_storage_api(self):
        forbidden = {
            "storage.py",
            "storage_service.py",
            "storage_client.py",
            "storage_backend.py",
        }
        found = {
            path.name
            for path in (self.apps_root / "documents").rglob("*.py")
            if path.name in forbidden
        }
        self.assertEqual(found, set())

    def test_registry_has_no_retired_document_dependency(self):
        registry = self.storage_root / "registry.py"
        if registry.exists():
            text = registry.read_text(encoding="utf-8")
            self.assertNotIn("apps.common.documents", text)
