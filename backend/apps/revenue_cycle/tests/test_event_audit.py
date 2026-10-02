"""Semantic event-boundary audit for Revenue Cycle."""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase

REVENUE_CYCLE_ROOT = Path(__file__).resolve().parents[1]
PROTECTED_CONTEXTS = frozenset({"coding", "claim_scrubbing"})
ALLOWED_EXTERNAL_PUBLISH_PATTERNS = (
    "publish_after_commit(",
    "transaction.on_commit(",
)


def _protected(path: Path) -> bool:
    try:
        relative = path.relative_to(REVENUE_CYCLE_ROOT)
    except ValueError:
        return False
    return bool(relative.parts) and relative.parts[0] in PROTECTED_CONTEXTS


class RevenueCycleEventAuditTests(SimpleTestCase):
    """Verify event publication is deferred until commit."""

    def test_active_event_contexts_have_commit_boundary(self) -> None:
        violations = []
        for event_path in REVENUE_CYCLE_ROOT.rglob("events.py"):
            if _protected(event_path):
                continue

            context_root = event_path.parent.parent
            sources = [
                path
                for path in context_root.rglob("*.py")
                if "tests" not in path.parts
                and "migrations" not in path.parts
                and path.name != "__init__.py"
            ]
            combined = "\n".join(path.read_text(encoding="utf-8") for path in sources)

            if not any(
                token in combined for token in ALLOWED_EXTERNAL_PUBLISH_PATTERNS
            ):
                violations.append(str(event_path))

            if "DomainEvent.publish(" in combined:
                violations.append(f"{event_path}: direct DomainEvent.publish() bypass")

        self.assertEqual(violations, [])

    def test_services_do_not_bypass_with_direct_broker_calls(self) -> None:
        forbidden = (
            "kafka.",
            "pika.",
            "boto3.client(",
            "requests.post(",
            "requests.put(",
        )
        violations = []

        for path in REVENUE_CYCLE_ROOT.rglob("services.py"):
            if _protected(path):
                continue
            source = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in source:
                    violations.append(f"{path}: {token}")

        self.assertEqual(violations, [])


__all__ = ("RevenueCycleEventAuditTests",)
