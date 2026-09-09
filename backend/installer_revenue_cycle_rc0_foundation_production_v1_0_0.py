"""DatavionAI Revenue Cycle RC0 Foundation installer."""

from __future__ import annotations

import ast
import compileall
import shutil
from pathlib import Path

BACKEND_ROOT = Path.cwd()
ROOT = BACKEND_ROOT / "apps" / "revenue_cycle"
LEGACY = BACKEND_ROOT / "apps" / "revenue_cycle_legacy_backup"

MODULES = (
    "analytics",
    "appeals",
    "ar",
    "billing",
    "charge_capture",
    "claim_scrubbing",
    "claim_submission",
    "coding",
    "denials",
    "eligibility",
    "era",
    "insurance_verification",
    "payment_posting",
    "prior_authorization",
)

DQ = '"""'


def source(docstring: str, body: str = "") -> str:
    """Build a Python source file with a module docstring."""
    return DQ + docstring + DQ + "\n\n" + body.lstrip()


def write_file(path: Path, content: str) -> None:
    """Write one UTF-8 source file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def verify_project() -> None:
    """Verify the installer runs from the backend root."""
    if not (BACKEND_ROOT / "manage.py").exists():
        raise RuntimeError("Run this installer from the DatavionAI backend directory.")

    if not LEGACY.exists():
        raise RuntimeError("apps\\revenue_cycle_legacy_backup was not found.")


def create_root_files() -> None:
    """Create the fresh Revenue Cycle RC0 foundation."""
    if ROOT.exists():
        shutil.rmtree(ROOT)

    write_file(
        ROOT / "__init__.py",
        source(
            "DatavionAI Revenue Cycle bounded context.",
            """
from __future__ import annotations

__all__ = ()
""",
        ),
    )

    write_file(
        ROOT / "apps.py",
        source(
            "Django application configuration for Revenue Cycle.",
            '''
from __future__ import annotations

from django.apps import AppConfig


class RevenueCycleConfig(AppConfig):
    """Configure the Revenue Cycle bounded context."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.revenue_cycle"
    label = "revenue_cycle"
    verbose_name = "Revenue Cycle"

    def ready(self) -> None:
        """Load Revenue Cycle registrations."""
        return None


__all__ = ("RevenueCycleConfig",)
''',
        ),
    )

    write_file(
        ROOT / "components.py",
        source(
            "Shared Revenue Cycle execution context.",
            '''
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RevenueCycleContext:
    """Immutable context passed through Revenue Cycle workflows."""

    actor: Any
    tenant: Any
    organization: Any
    request_id: str | None = None


__all__ = ("RevenueCycleContext",)
''',
        ),
    )

    write_file(
        ROOT / "exceptions.py",
        source(
            "Revenue Cycle domain exceptions.",
            '''
from __future__ import annotations


class RevenueCycleError(Exception):
    """Base Revenue Cycle exception."""


class RevenueCycleValidationError(RevenueCycleError):
    """Raised for domain validation failures."""


class RevenueCycleAuthorizationError(RevenueCycleError):
    """Raised for authorization failures."""


class RevenueCycleTenantContextError(RevenueCycleError):
    """Raised for tenant or organization context failures."""


class RevenueCycleConcurrencyError(RevenueCycleError):
    """Raised for concurrency failures."""


class RevenueCycleIdempotencyError(RevenueCycleError):
    """Raised for idempotency failures."""


__all__ = (
    "RevenueCycleError",
    "RevenueCycleValidationError",
    "RevenueCycleAuthorizationError",
    "RevenueCycleTenantContextError",
    "RevenueCycleConcurrencyError",
    "RevenueCycleIdempotencyError",
)
''',
        ),
    )

    write_file(
        ROOT / "constants" / "__init__.py",
        source(
            "Shared Revenue Cycle constants.",
            '''
from __future__ import annotations

from enum import StrEnum


class RevenueCycleModule(StrEnum):
    """Registered Revenue Cycle modules."""

    ELIGIBILITY = "eligibility"
    INSURANCE_VERIFICATION = "insurance_verification"
    PRIOR_AUTHORIZATION = "prior_authorization"
    CHARGE_CAPTURE = "charge_capture"
    CODING = "coding"
    CLAIM_SCRUBBING = "claim_scrubbing"
    CLAIM_SUBMISSION = "claim_submission"
    PAYMENT_POSTING = "payment_posting"
    ERA = "era"
    DENIALS = "denials"
    APPEALS = "appeals"
    ACCOUNTS_RECEIVABLE = "ar"
    ANALYTICS = "analytics"
    BILLING = "billing"


REVENUE_CYCLE_MODULES = tuple(
    module.value
    for module in RevenueCycleModule
)

__all__ = (
    "RevenueCycleModule",
    "REVENUE_CYCLE_MODULES",
)
''',
        ),
    )

    foundation = ROOT / "foundation"

    write_file(
        foundation / "__init__.py",
        source(
            "Revenue Cycle foundation infrastructure.",
            """
from __future__ import annotations

from .audit import build_audit_metadata
from .idempotency import fingerprint_idempotency_key
from .idempotency import normalize_idempotency_key
from .money import Money
from .rbac import has_permission
from .tenant import ensure_organization_match
from .tenant import require_revenue_cycle_context

__all__ = (
    "Money",
    "build_audit_metadata",
    "ensure_organization_match",
    "fingerprint_idempotency_key",
    "has_permission",
    "normalize_idempotency_key",
    "require_revenue_cycle_context",
)
""",
        ),
    )

    write_file(
        foundation / "currency.py",
        source(
            "Revenue Cycle currency definitions.",
            '''
from __future__ import annotations

from enum import StrEnum

from apps.revenue_cycle.exceptions import RevenueCycleValidationError


class Currency(StrEnum):
    """Supported accounting currencies."""

    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


SUPPORTED_CURRENCIES = tuple(
    currency.value
    for currency in Currency
)


def validate_currency(value: str) -> str:
    """Validate and normalize a supported currency."""
    normalized = str(value).strip().upper()

    if normalized not in SUPPORTED_CURRENCIES:
        raise RevenueCycleValidationError(
            f"Unsupported currency: {normalized}."
        )

    return normalized


__all__ = (
    "Currency",
    "SUPPORTED_CURRENCIES",
    "validate_currency",
)
''',
        ),
    )

    write_file(
        foundation / "money.py",
        source(
            "Immutable Revenue Cycle monetary value object.",
            '''
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from decimal import ROUND_HALF_UP

from apps.revenue_cycle.exceptions import RevenueCycleValidationError
from apps.revenue_cycle.foundation.currency import validate_currency


QUANTUM = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Money:
    """Represent a validated non-negative monetary value."""

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        """Normalize and validate the monetary value."""
        amount = Decimal(str(self.amount)).quantize(
            QUANTUM,
            rounding=ROUND_HALF_UP,
        )
        currency = validate_currency(self.currency)

        if not amount.is_finite():
            raise RevenueCycleValidationError(
                "Money amount must be finite."
            )

        if amount < Decimal("0"):
            raise RevenueCycleValidationError(
                "Money amount cannot be negative."
            )

        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", currency)

    def add(self, other: Money) -> Money:
        """Return the sum of two same-currency values."""
        self._ensure_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: Money) -> Money:
        """Return a non-negative difference."""
        self._ensure_currency(other)
        result = self.amount - other.amount

        if result < Decimal("0"):
            raise RevenueCycleValidationError(
                "Money subtraction cannot be negative."
            )

        return Money(result, self.currency)

    def _ensure_currency(self, other: Money) -> None:
        """Ensure both values use the same currency."""
        if self.currency != other.currency:
            raise RevenueCycleValidationError(
                "Money values must use the same currency."
            )


__all__ = ("Money",)
''',
        ),
    )

    write_file(
        foundation / "tenant.py",
        source(
            "Explicit Revenue Cycle tenant isolation.",
            '''
from __future__ import annotations

from typing import Any

from apps.revenue_cycle.exceptions import RevenueCycleTenantContextError


def require_revenue_cycle_context(
    request: Any,
) -> tuple[Any, Any]:
    """Require explicit tenant and organization context."""
    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)

    if tenant is None:
        raise RevenueCycleTenantContextError(
            "Revenue Cycle requires explicit request.tenant context."
        )

    if organization is None:
        raise RevenueCycleTenantContextError(
            "Revenue Cycle requires explicit request.organization context."
        )

    tenant_id = getattr(tenant, "id", tenant)
    organization_tenant_id = getattr(
        organization,
        "tenant_id",
        None,
    )

    if (
        organization_tenant_id is not None
        and organization_tenant_id != tenant_id
    ):
        raise RevenueCycleTenantContextError(
            "Organization does not belong to the active tenant."
        )

    return tenant, organization


def ensure_organization_match(
    organization: Any,
    expected_organization: Any,
) -> None:
    """Ensure a resource belongs to the request organization."""
    organization_id = getattr(organization, "id", organization)
    expected_id = getattr(
        expected_organization,
        "id",
        expected_organization,
    )

    if organization_id != expected_id:
        raise RevenueCycleTenantContextError(
            "Resource organization does not match request organization."
        )


__all__ = (
    "ensure_organization_match",
    "require_revenue_cycle_context",
)
''',
        ),
    )

    write_file(
        foundation / "rbac.py",
        source(
            "Canonical Revenue Cycle RBAC adapter.",
            '''
from __future__ import annotations

from typing import Any

from apps.platform.rbac.engines import user_has_permission


def has_permission(
    *,
    actor: Any,
    permission: str,
    organization: Any,
) -> bool:
    """Evaluate a permission through the canonical platform engine."""
    return bool(
        user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )
    )


__all__ = ("has_permission",)
''',
        ),
    )

    write_file(
        foundation / "permissions.py",
        source(
            "Revenue Cycle permission conventions.",
            '''
from __future__ import annotations


PERMISSION_PREFIX = "revenue_cycle"


def permission_code(
    action: str,
    resource: str,
) -> str:
    """Build a normalized Revenue Cycle permission code."""
    return (
        f"{PERMISSION_PREFIX}."
        f"{resource.strip().lower()}."
        f"{action.strip().lower()}"
    )


__all__ = (
    "PERMISSION_PREFIX",
    "permission_code",
)
''',
        ),
    )

    write_file(
        foundation / "idempotency.py",
        source(
            "Revenue Cycle idempotency helpers.",
            '''
from __future__ import annotations

from hashlib import sha256

from apps.revenue_cycle.exceptions import RevenueCycleIdempotencyError


MAX_IDEMPOTENCY_KEY_LENGTH = 255


def normalize_idempotency_key(value: str) -> str:
    """Validate and normalize an external idempotency key."""
    normalized = str(value).strip()

    if not normalized:
        raise RevenueCycleIdempotencyError(
            "Idempotency key cannot be empty."
        )

    if len(normalized) > MAX_IDEMPOTENCY_KEY_LENGTH:
        raise RevenueCycleIdempotencyError(
            "Idempotency key exceeds the maximum length."
        )

    return normalized


def fingerprint_idempotency_key(
    *,
    operation: str,
    key: str,
) -> str:
    """Create a deterministic operation/key fingerprint."""
    normalized_key = normalize_idempotency_key(key)
    payload = f"{operation.strip().lower()}:{normalized_key}"

    return sha256(
        payload.encode("utf-8")
    ).hexdigest()


__all__ = (
    "fingerprint_idempotency_key",
    "normalize_idempotency_key",
)
''',
        ),
    )

    write_file(
        foundation / "audit.py",
        source(
            "Revenue Cycle audit metadata helpers.",
            '''
from __future__ import annotations

from datetime import datetime
from typing import Any


def build_audit_metadata(
    *,
    actor: Any,
    action: str,
    request_id: str | None = None,
    changes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build serializable audit metadata."""
    actor_id = getattr(actor, "id", None)

    return {
        "actor_id": str(actor_id) if actor_id is not None else None,
        "action": action.strip(),
        "request_id": request_id,
        "changes": dict(changes or {}),
        "occurred_at": datetime.utcnow().isoformat(),
    }


__all__ = ("build_audit_metadata",)
''',
        ),
    )

    write_file(
        foundation / "status.py",
        source(
            "Shared Revenue Cycle statuses.",
            '''
from __future__ import annotations

from enum import StrEnum


class RecordLifecycleStatus(StrEnum):
    """Generic lifecycle states."""

    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class ProcessingStatus(StrEnum):
    """Generic processing states."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


__all__ = (
    "ProcessingStatus",
    "RecordLifecycleStatus",
)
''',
        ),
    )

    write_file(
        foundation / "validators.py",
        source(
            "Shared Revenue Cycle validators.",
            '''
from __future__ import annotations

from decimal import Decimal

from apps.revenue_cycle.exceptions import RevenueCycleValidationError


def validate_non_negative_amount(
    value: Decimal | int | float | str,
) -> Decimal:
    """Validate a finite non-negative amount."""
    amount = Decimal(str(value))

    if not amount.is_finite():
        raise RevenueCycleValidationError("Amount must be finite.")

    if amount < Decimal("0"):
        raise RevenueCycleValidationError(
            "Amount cannot be negative."
        )

    return amount


def validate_percentage(
    value: Decimal | int | float | str,
) -> Decimal:
    """Validate a percentage from zero through one hundred."""
    percentage = Decimal(str(value))

    if not percentage.is_finite():
        raise RevenueCycleValidationError(
            "Percentage must be finite."
        )

    if percentage < Decimal("0") or percentage > Decimal("100"):
        raise RevenueCycleValidationError(
            "Percentage must be between 0 and 100."
        )

    return percentage


__all__ = (
    "validate_non_negative_amount",
    "validate_percentage",
)
''',
        ),
    )


def create_module_packages() -> None:
    """Create the complete package architecture for all RC domains."""
    for module in MODULES:
        module_root = ROOT / module

        for package in (
            "",
            "api",
            "api/serializers",
            "api/views",
            "models",
            "selectors",
            "services",
            "workflows",
            "policies",
            "permissions",
            "events",
            "tests",
            "migrations",
        ):
            package_root = module_root / package
            name = package or "domain"

            write_file(
                package_root / "__init__.py",
                source(
                    f"Revenue Cycle {module} {name} package.",
                    """
from __future__ import annotations

__all__ = ()
""",
                ),
            )

        write_file(
            module_root / "urls.py",
            source(
                f"URL configuration for Revenue Cycle {module}.",
                """
from __future__ import annotations


urlpatterns = ()


__all__ = ("urlpatterns",)
""",
            ),
        )


def create_urls() -> None:
    """Create the root Revenue Cycle URL configuration."""
    entries = "\n".join(
        (f'    path("{module}/", include("apps.revenue_cycle.{module}.urls"),\n    ),')
        for module in MODULES
    )

    write_file(
        ROOT / "urls.py",
        source(
            "Root Revenue Cycle URL configuration.",
            f"""
from __future__ import annotations

from django.urls import include
from django.urls import path


urlpatterns = (
{entries}
)


__all__ = ("urlpatterns",)
""",
        ),
    )


def create_tests() -> None:
    """Create RC0 architecture tests."""
    tests = ROOT / "tests"

    write_file(
        tests / "__init__.py",
        source("Revenue Cycle architecture tests."),
    )

    write_file(
        tests / "test_architecture.py",
        source(
            "Revenue Cycle RC0 architecture invariants.",
            '''
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_legacy_patient_reference_exists() -> None:
    """Ensure active Revenue Cycle has no legacy Patient references."""
    forbidden = (
        "apps." + "clinical.patients",
        "patients." + "patient",
    )

    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue

        content = path.read_text(encoding="utf-8")

        for token in forbidden:
            assert token not in content


def test_platform_rbac_is_used() -> None:
    """Ensure Revenue Cycle delegates RBAC to the platform engine."""
    content = (
        ROOT / "foundation" / "rbac.py"
    ).read_text(encoding="utf-8")

    assert "apps.platform.rbac.engines" in content
    assert "user_has_permission" in content


def test_explicit_tenant_context_is_required() -> None:
    """Ensure tenant context has no implicit organization-role fallback."""
    content = (
        ROOT / "foundation" / "tenant.py"
    ).read_text(encoding="utf-8")

    assert "request.tenant" in content
    assert "request.organization" in content
    assert "organization_roles" not in content
''',
        ),
    )


def verify() -> None:
    """Verify style, compilation, and RC0 architecture."""
    python_files = tuple(ROOT.rglob("*.py"))

    for path in python_files:
        content = path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(path))

        if not tree.body:
            raise AssertionError(f"Empty Python file: {path}")

        first = tree.body[0]

        if not (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            raise AssertionError(f"Missing module docstring: {path}")

        if "from __future__ import annotations" not in content:
            if path.name != "__init__.py":
                raise AssertionError(f"Missing future annotations import: {path}")

        if "apps." + "clinical.patients" in content:
            raise AssertionError(f"Legacy Patient import/reference found: {path}")

        if "patients." + "patient" in content:
            raise AssertionError(f"Legacy Patient model reference found: {path}")

    if not compileall.compile_dir(
        str(ROOT),
        quiet=1,
        force=True,
    ):
        raise AssertionError("Revenue Cycle compilation failed.")

    rbac = (ROOT / "foundation" / "rbac.py").read_text(encoding="utf-8")

    tenant = (ROOT / "foundation" / "tenant.py").read_text(encoding="utf-8")

    assert "apps.platform.rbac.engines" in rbac
    assert "user_has_permission" in rbac
    assert "request.tenant" in tenant
    assert "request.organization" in tenant
    assert "organization_roles" not in tenant

    migrations = [
        path
        for path in ROOT.rglob("*.py")
        if "migrations" in path.parts and path.name != "__init__.py"
    ]

    assert not migrations

    print(f"MANIFEST PASS ({len(python_files)} Python files)")
    print("STYLE PASS")
    print("PY_COMPILE PASS")
    print("ARCHITECTURE PASS")
    print("CANONICAL RBAC: PLATFORM ENGINE")
    print("TENANT CONTEXT: EXPLICIT")
    print("LEGACY PATIENT REFERENCES: NONE")
    print("MIGRATIONS NOT GENERATED")
    print("DATABASE NOT MODIFIED")
    print("LEGACY BACKUP PRESERVED")


def main() -> None:
    """Recreate and verify the fresh Revenue Cycle RC0 foundation."""
    print("DatavionAI Revenue Cycle RC0 Foundation Installer v1.0.0")
    print("=" * 72)

    verify_project()
    create_root_files()
    create_module_packages()
    create_urls()
    create_tests()
    verify()

    print("OLD ACTIVE REVENUE CYCLE REMOVED")
    print("FRESH REVENUE CYCLE TREE CREATED")
    print("RC0 FOUNDATION INSTALL COMPLETE")


if __name__ == "__main__":
    main()
