import unittest
from pathlib import Path


class DepartmentScopedAIControlPlaneArchitectureTests(unittest.TestCase):
    """
    Django unittest-discoverable architecture contract tests.

    These tests intentionally validate architectural ownership and
    boundaries without creating or modifying database schema.
    """

    @staticmethod
    def project_root() -> Path:
        return Path(__file__).resolve().parents[1]

    def read_service(self) -> str:
        return (self.project_root() / "ai_control" / "service.py").read_text(
            encoding="utf-8"
        )

    def read_views(self) -> str:
        return (self.project_root() / "ai_control" / "api" / "views.py").read_text(
            encoding="utf-8"
        )

    def test_ai_owner_is_canonical_apps_ai(self):
        source = self.read_service()

        self.assertIn(
            "from apps.ai.models import AIApplication",
            source,
        )

    def test_ai_requires_saas_and_org_state(self):
        source = self.read_service()

        self.assertIn(
            "EntitlementService.has_module",
            source,
        )

        self.assertIn(
            "EntitlementService.has_feature",
            source,
        )

        self.assertIn(
            "module_enabled",
            source,
        )

        self.assertIn(
            "feature_enabled",
            source,
        )

        self.assertIn(
            "application.status",
            source,
        )

    def test_ai_requires_rbac_and_department(self):
        source = self.read_service()

        self.assertIn(
            "user_has_permission",
            source,
        )

        self.assertIn(
            "DepartmentMember",
            source,
        )

        self.assertIn(
            "department__organization",
            source,
        )

    def test_ai_toggle_is_organization_scoped(self):
        source = self.read_views()

        self.assertIn(
            "tenant=organization.tenant",
            source,
        )

        self.assertIn(
            "organization=organization",
            source,
        )

    def test_no_new_schema_model(self):
        source = self.read_service()

        self.assertNotIn(
            "models.Model",
            source,
        )

        self.assertNotIn(
            "models.ForeignKey",
            source,
        )


if __name__ == "__main__":
    unittest.main()
