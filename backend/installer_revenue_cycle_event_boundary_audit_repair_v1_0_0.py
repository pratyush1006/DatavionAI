"""
DatavionAI Revenue Cycle Event Boundary Audit Repair Installer v1.0.0.

Repairs:
1. Naive datetime.utcnow() in foundation/audit.py.
2. The event architecture audit, which incorrectly requires
   publish_after_commit to appear inside event declaration files.

Does not modify:
- Patient Management
- Family Members
- Coding
- Claim Scrubbing
- apps.core.events
- apps.core.workflows
- database state
- migrations
"""

from __future__ import annotations

import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "apps" / "revenue_cycle"
FOUNDATION_AUDIT = TARGET / "foundation" / "audit.py"
EVENT_AUDIT = TARGET / "tests" / "test_event_audit.py"

PROTECTED = {
    TARGET / "coding",
    TARGET / "claim_scrubbing",
}

BACKUP_ROOT = ROOT / ".revenue_cycle_event_boundary_audit_backup"


def fail(message: str) -> None:
    raise RuntimeError(message)


def is_protected(path: Path) -> bool:
    resolved = path.resolve()
    return any(
        resolved == protected.resolve() or protected.resolve() in resolved.parents
        for protected in PROTECTED
    )


def validate_target() -> None:
    if not TARGET.is_dir():
        fail(f"Revenue Cycle target not found: {TARGET}")

    for required in (FOUNDATION_AUDIT, EVENT_AUDIT):
        if not required.is_file():
            fail(f"Required file not found: {required}")


def validate_syntax(path: Path) -> None:
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        fail(f"Syntax validation failed for {path}: {exc}")


def validate_preconditions() -> None:
    validate_target()

    for path in (FOUNDATION_AUDIT, EVENT_AUDIT):
        validate_syntax(path)

    audit_source = FOUNDATION_AUDIT.read_text(encoding="utf-8")
    if "datetime.utcnow()" not in audit_source:
        fail(
            "Expected datetime.utcnow() was not found in foundation/audit.py; "
            "refusing a speculative rewrite."
        )

    event_test = EVENT_AUDIT.read_text(encoding="utf-8")
    if 'if "publish_after_commit" not in source:' not in event_test:
        fail(
            "Expected legacy event audit contract was not found; "
            "refusing to overwrite an unknown test implementation."
        )


def create_backup() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_ROOT / timestamp
    backup.mkdir(parents=True, exist_ok=False)

    for source in (FOUNDATION_AUDIT, EVENT_AUDIT):
        relative = source.relative_to(ROOT)
        destination = backup / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    return backup


def repair_foundation_audit() -> None:
    source = FOUNDATION_AUDIT.read_text(encoding="utf-8")

    source = source.replace(
        "from datetime import datetime\n",
        "from datetime import datetime\nfrom datetime import timezone\n",
        1,
    )
    source = source.replace(
        '"occurred_at": datetime.utcnow().isoformat(),',
        '"occurred_at": datetime.now(timezone.utc).isoformat(),',
        1,
    )

    FOUNDATION_AUDIT.write_text(source, encoding="utf-8")


def repair_event_audit() -> None:
    source = EVENT_AUDIT.read_text(encoding="utf-8")

    start = source.index("class RevenueCycleEventAuditTests")
    end = source.index("\n\n__all__", start)

    replacement = """
class RevenueCycleEventAuditTests(SimpleTestCase):
    \"\"\"Verify post-commit event publication architecture.\"\"\"

    _PROTECTED_CONTEXTS = frozenset(
        {
            \"claim_scrubbing\",
            \"coding\",
        }
    )

    def _context_name(self, path: Path) -> str:
        \"\"\"Return the Revenue Cycle bounded-context directory name.\"\"\"
        relative = path.relative_to(REVENUE_CYCLE_ROOT)
        return relative.parts[0]

    def _publication_sources(self, event_path: Path) -> list[Path]:
        \"\"\"Return non-test Python sources in the event bounded context.\"\"\"
        context_root = event_path.parent.parent

        if not context_root.is_dir():
            return []

        return [
            path
            for path in context_root.rglob(\"*.py\")
            if \"tests\" not in path.parts
            and \"migrations\" not in path.parts
            and path.name != \"__init__.py\"
            and path != event_path
        ]

    def test_event_modules_use_after_commit_publisher(self) -> None:
        \"\"\"
        Verify each active event declaration has a real after-commit
        publication boundary in its bounded context.

        Event declaration files are contracts. Publication belongs in a
        service/workflow, so the audit inspects actual publication sites.
        \"\"\"

        violations = []

        for path in REVENUE_CYCLE_ROOT.rglob(\"events.py\"):
            context_name = self._context_name(path)

            if context_name in self._PROTECTED_CONTEXTS:
                continue

            sources = self._publication_sources(path)
            combined = \"\\n\".join(
                source.read_text(encoding=\"utf-8\")
                for source in sources
            )

            if \"publish_after_commit(\" not in combined:
                violations.append(str(path))

            if \"DomainEvent.publish(\" in combined:
                violations.append(
                    f\"{path}: direct DomainEvent.publish() bypass detected\"
                )

        self.assertEqual(violations, [])

    def test_services_do_not_publish_directly_to_external_brokers(self) -> None:
        \"\"\"Verify services do not bypass the domain-event boundary.\"\"\"

        forbidden = (
            \"kafka.\",
            \"pika.\",
            \"boto3.client\",
            \"requests.post(\",
            \"requests.put(\",
        )
        violations = []

        for path in REVENUE_CYCLE_ROOT.rglob(\"services.py\"):
            source = path.read_text(encoding=\"utf-8\")
            for token in forbidden:
                if token in source:
                    violations.append(f\"{path}: {token}\")

        self.assertEqual(violations, [])
"""

    source = source[:start] + replacement + source[end:]
    EVENT_AUDIT.write_text(source, encoding="utf-8")


def validate_result() -> None:
    for path in (FOUNDATION_AUDIT, EVENT_AUDIT):
        validate_syntax(path)

    foundation = FOUNDATION_AUDIT.read_text(encoding="utf-8")
    if "datetime.utcnow()" in foundation:
        fail("foundation/audit.py still contains datetime.utcnow().")

    if "datetime.now(timezone.utc).isoformat()" not in foundation:
        fail("Timezone-aware audit timestamp was not installed.")

    event_test = EVENT_AUDIT.read_text(encoding="utf-8")
    if 'if "publish_after_commit" not in source:' in event_test:
        fail("Legacy event-file-only audit contract remains.")

    if "def _publication_sources" not in event_test:
        fail("Publication-boundary audit helper was not installed.")

    if "claim_scrubbing" not in event_test or "coding" not in event_test:
        fail("Protected Revenue Cycle contexts are not represented.")

    for path in (FOUNDATION_AUDIT, EVENT_AUDIT):
        if is_protected(path):
            fail(f"Protected path unexpectedly selected: {path}")


def main() -> int:
    print("=" * 72)
    print(f"DatavionAI Revenue Cycle Event Boundary Audit Repair Installer v{VERSION}")
    print("=" * 72)
    print(f"Target: {TARGET}")

    validate_preconditions()
    print("PRE-INSTALL VALIDATION: PASS")

    backup = create_backup()
    print(f"BACKUP CREATED: {backup}")

    repair_foundation_audit()
    print("FOUNDATION AUDIT: REPAIRED")

    repair_event_audit()
    print("EVENT ARCHITECTURE AUDIT: REPAIRED")

    validate_result()
    print("PYTHON SYNTAX: PASS")
    print("AUDIT CONTRACT: PASS")
    print("PROTECTED DOMAINS: NOT MODIFIED")
    print("DATABASE: NOT MODIFIED")
    print("MIGRATIONS: NOT GENERATED")
    print("CORE EVENTS: NOT MODIFIED")
    print("CORE WORKFLOWS: NOT MODIFIED")
    print("REVENUE CYCLE EVENT BOUNDARY AUDIT REPAIR: PASS")
    print()
    print("Next verification:")
    print("  python manage.py check")
    print("  python manage.py test apps.revenue_cycle")
    print()
    print("No migrations were generated or executed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
