"""Domain-event architecture audit for Revenue Cycle."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_CONTEXTS = frozenset({"coding", "claim_scrubbing"})


class RevenueCycleEventAuditTests(SimpleTestCase):
    """Verify post-commit event publication architecture."""

    def test_event_modules_use_after_commit_publisher(self) -> None:
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("events.py"):
            relative = path.relative_to(REVENUE_CYCLE_ROOT)
            if not relative.parts or relative.parts[0] in PROTECTED_CONTEXTS:
                continue
            context_root = path.parent.parent
            sources = [
                source_path
                for source_path in context_root.rglob("*.py")
                if "tests" not in source_path.parts
                and "migrations" not in source_path.parts
                and source_path.name != "__init__.py"
                and source_path != path
            ]
            combined = "\n".join(
                source_path.read_text(encoding="utf-8") for source_path in sources
            )
            if "publish_after_commit(" not in combined:
                violations.append(str(path))
        self.assertEqual(violations, [])

    def test_services_do_not_publish_directly_to_external_brokers(self) -> None:
        forbidden = (
            "kafka.",
            "pika.",
            "boto3.client",
            "requests.post(",
            "requests.put(",
        )
        violations = []
        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if any(part in PROTECTED_CONTEXTS for part in path.parts):
                continue
            source = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in source:
                    violations.append(f"{path}: {token}")
        self.assertEqual(violations, [])


__all__ = ("RevenueCycleEventAuditTests",)
