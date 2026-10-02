"""Generated Provider permission contract tests for forward repair."""

from django.test import SimpleTestCase


class ProviderPermissionContractTests(SimpleTestCase):
    def test_provider_permission_module_uses_canonical_rbac(self):
        from pathlib import Path

        path = Path(__file__).resolve().parents[1] / "permissions" / "provider.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("apps.platform.rbac.resolvers", source)
        self.assertIn("resolve_permissions", source)
        self.assertNotIn("apps.platform.rbac." + "engines", source)
