"""Architecture tests for claim scrubbing."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class ClaimScrubbingArchitectureTests(SimpleTestCase):
    """Verify critical architectural source boundaries."""

    def test_selector_contains_row_locking(self):
        """Ensure mutation selector uses select_for_update."""

        source = Path(__file__).resolve().parents[1] / "selectors.py"
        self.assertIn("select_for_update", source.read_text(encoding="utf-8"))

    def test_policy_uses_platform_rbac(self):
        """Ensure policy delegates to the canonical RBAC engine."""

        source = Path(__file__).resolve().parents[1] / "policies.py"
        self.assertIn(
            "apps.platform.rbac.resolvers", source.read_text(encoding="utf-8")
        )

    def test_patient_reference_is_canonical(self):
        """Ensure no legacy clinical patient import is introduced."""

        root = Path(__file__).resolve().parents[1]
        for path in root.rglob("*.py"):
            self.assertNotIn(
                "apps.clinical.patients.models", path.read_text(encoding="utf-8")
            )


__all__ = ("ClaimScrubbingArchitectureTests",)
