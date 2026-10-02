"""Architecture tests for claim scrubbing."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class ClaimScrubbingArchitectureTests(SimpleTestCase):
    """Verify critical architectural source boundaries."""

    def test_selector_contains_row_locking(self) -> None:
        """Ensure the mutation selector uses select_for_update."""

        source = Path(__file__).resolve().parents[1] / "selectors.py"
        self.assertIn("select_for_update", source.read_text(encoding="utf-8"))

    def test_policy_uses_platform_rbac(self) -> None:
        """Ensure policy delegates directly to the canonical platform RBAC resolver."""

        source = Path(__file__).resolve().parents[1] / "policies.py"
        text = source.read_text(encoding="utf-8")

        self.assertIn(
            "from apps.platform.rbac.resolvers import resolve_permissions",
            text,
        )
        self.assertIn("resolve_permissions(", text)

    def test_patient_reference_is_canonical(self) -> None:
        """Ensure production files do not reference the retired patient module."""

        root = Path(__file__).resolve().parents[1]

        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue

            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "apps.clinical.patients.models",
                text,
                msg=f"Legacy patient dependency found in {path}",
            )


__all__ = ("ClaimScrubbingArchitectureTests",)
