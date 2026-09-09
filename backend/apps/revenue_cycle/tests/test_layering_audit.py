"""Layering and dependency audit for Revenue Cycle."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_CONTEXTS = frozenset({"coding", "claim_scrubbing"})


def _protected(path: Path) -> bool:
    try:
        relative = path.relative_to(REVENUE_CYCLE_ROOT)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in PROTECTED_CONTEXTS


def _transactional(source: str) -> bool:
    return (
        "@transaction.atomic" in source
        or "with transaction.atomic(" in source
        or "with transaction.atomic():" in source
    )


def _organization_scoped(source: str) -> bool:
    return any(
        token in source
        for token in (
            "organization_id",
            "organization=organization",
            "organization = organization",
            "organization__id",
            "for_organization(",
            "filter(organization",
            "get(organization",
        )
    )


class RevenueCycleLayeringAuditTests(SimpleTestCase):
    """Verify the agreed Revenue Cycle runtime layering."""

    def test_mutation_modules_contain_workflow_policy_service_layers(self) -> None:
        missing = []
        for module_path in REVENUE_CYCLE_ROOT.iterdir():
            if not module_path.is_dir() or module_path.name in {"tests", "migrations"}:
                continue
            for filename in ("workflows", "policies", "services"):
                candidate = module_path / f"{filename}.py"
                if (
                    candidate.exists()
                    and not candidate.read_text(encoding="utf-8").strip()
                ):
                    missing.append(str(candidate))
        self.assertEqual(missing, [])

    def test_selectors_are_organization_scoped(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("selectors.py"):
            if not _protected(path) and not _organization_scoped(
                path.read_text(encoding="utf-8")
            ):
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_mutating_services_use_transactions(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if not _protected(path) and not _transactional(
                path.read_text(encoding="utf-8")
            ):
                violations.append(str(path))
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleLayeringAuditTests",)
