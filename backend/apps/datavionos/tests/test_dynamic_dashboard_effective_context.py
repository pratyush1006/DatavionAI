import unittest
from pathlib import Path


class DynamicDashboardEffectiveContextTests(unittest.TestCase):
    @staticmethod
    def root() -> Path:
        return Path(__file__).resolve().parents[1]

    def read(
        self,
        relative_path: str,
    ) -> str:
        return (self.root() / relative_path).read_text(encoding="utf-8")

    def test_effective_context_is_canonical_authority(self):
        source = self.read("services/effective_capability.py")

        self.assertIn(
            "class EffectiveCapabilityContext",
            source,
        )

        self.assertIn(
            "def module_enabled",
            source,
        )

        self.assertIn(
            "def feature_enabled",
            source,
        )

        self.assertIn(
            "def has_permission",
            source,
        )

    def test_dashboard_consumes_effective_context(self):
        source = self.read("builders/dashboard.py")

        self.assertIn(
            "effective_context",
            source,
        )

        self.assertIn(
            "effective_context.module_enabled",
            source,
        )

        self.assertIn(
            "effective_context.feature_enabled",
            source,
        )

        self.assertIn(
            "effective_context.has_any_permission",
            source,
        )

    def test_navigation_consumes_effective_context(self):
        source = self.read("builders/navigation.py")

        self.assertIn(
            "effective_context",
            source,
        )

        self.assertIn(
            "effective_context.module_enabled",
            source,
        )

        self.assertIn(
            "effective_context.feature_enabled",
            source,
        )

        self.assertIn(
            "effective_context.has_any_permission",
            source,
        )

    def test_bootstrap_composes_single_context(self):
        source = self.read("bootstrap/service.py")

        self.assertIn(
            "build_effective_capability_context",
            source,
        )

        self.assertIn(
            "effective_context=effective_context",
            source,
        )

    def test_frontend_is_not_authorization_authority(self):
        frontend_root = self.root().parents[2] / "frontend" / "src"

        if not frontend_root.exists():
            self.skipTest("Frontend source root unavailable.")

        forbidden = (
            "subscription ===",
            "plan ===",
            "isHospital",
            "isClinic",
            "organizationType ===",
        )

        violations = []

        for path in frontend_root.rglob("*.tsx"):
            text = path.read_text(encoding="utf-8")

            for token in forbidden:
                if token in text:
                    violations.append(f"{path}: {token}")

        self.assertEqual(
            violations,
            [],
        )


if __name__ == "__main__":
    unittest.main()
