"""DatavionOS Billing Foundation installer. Version 1.0.0."""

from __future__ import annotations

import py_compile
import sys
import textwrap
from pathlib import Path

VERSION = "1.0.0"
SOURCES = {
    "apps/billing/foundation/__init__.py": '''
"""DatavionOS Billing Foundation shared exports."""
from __future__ import annotations
from .currency import DEFAULT_CURRENCY, SUPPORTED_CURRENCIES
from .exceptions import BillingConfigurationError, BillingDomainError, BillingIntegrityError, BillingNotFoundError, BillingPermissionError, BillingStateError, BillingValidationError
from .money import ZERO_MONEY, Money
from .tenant import require_billing_organization, require_billing_tenant
__all__ = ["BillingConfigurationError", "BillingDomainError", "BillingIntegrityError", "BillingNotFoundError", "BillingPermissionError", "BillingStateError", "BillingValidationError", "DEFAULT_CURRENCY", "Money", "SUPPORTED_CURRENCIES", "ZERO_MONEY", "require_billing_organization", "require_billing_tenant"]
''',
    "apps/billing/foundation/currency.py": '''
"""Billing currency definitions."""
from __future__ import annotations
DEFAULT_CURRENCY = "INR"
SUPPORTED_CURRENCIES = ("INR", "USD", "EUR", "GBP")
CURRENCY_DECIMAL_PLACES = {"INR": 2, "USD": 2, "EUR": 2, "GBP": 2}
def normalize_currency(currency: str) -> str:
    """Normalize and validate a currency code."""
    normalized = currency.strip().upper()
    if normalized not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Unsupported billing currency: {currency}")
    return normalized
def decimal_places(currency: str) -> int:
    """Return configured decimal precision."""
    return CURRENCY_DECIMAL_PLACES[normalize_currency(currency)]
__all__ = ["CURRENCY_DECIMAL_PLACES", "DEFAULT_CURRENCY", "SUPPORTED_CURRENCIES", "decimal_places", "normalize_currency"]
''',
    "apps/billing/foundation/money.py": '''
"""Immutable Decimal-based money value object."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from .currency import DEFAULT_CURRENCY, normalize_currency
@dataclass(frozen=True, slots=True)
class Money:
    """Represent a monetary amount with explicit currency."""
    amount: Decimal
    currency: str = DEFAULT_CURRENCY
    def __post_init__(self) -> None:
        """Normalize amount and currency."""
        object.__setattr__(self, "amount", Decimal(str(self.amount)))
        object.__setattr__(self, "currency", normalize_currency(self.currency))
    def _require_same_currency(self, other: Self) -> None:
        """Require matching currencies."""
        if self.currency != other.currency:
            raise ValueError("Cannot perform monetary arithmetic across currencies.")
    def add(self, other: Self) -> Self:
        """Add two same-currency amounts."""
        self._require_same_currency(other)
        return Self(self.amount + other.amount, self.currency)
    def subtract(self, other: Self) -> Self:
        """Subtract two same-currency amounts."""
        self._require_same_currency(other)
        return Self(self.amount - other.amount, self.currency)
    def multiply(self, factor: int | Decimal) -> Self:
        """Multiply an amount by a numeric factor."""
        return Self(self.amount * Decimal(str(factor)), self.currency)
    def is_zero(self) -> bool:
        """Return whether amount is zero."""
        return self.amount == Decimal("0")
    def is_positive(self) -> bool:
        """Return whether amount is positive."""
        return self.amount > Decimal("0")
    def is_negative(self) -> bool:
        """Return whether amount is negative."""
        return self.amount < Decimal("0")
ZERO_MONEY = Money(Decimal("0"))
__all__ = ["Money", "ZERO_MONEY"]
''',
    "apps/billing/foundation/exceptions.py": '''
"""Billing domain exceptions."""
from __future__ import annotations
class BillingDomainError(Exception):
    """Base Billing domain failure."""
class BillingConfigurationError(BillingDomainError):
    """Invalid Billing configuration."""
class BillingIntegrityError(BillingDomainError):
    """A financial invariant would be violated."""
class BillingNotFoundError(BillingDomainError):
    """A required Billing aggregate was not found."""
class BillingPermissionError(BillingDomainError):
    """A Billing operation is unauthorized."""
class BillingStateError(BillingDomainError):
    """A financial state transition is invalid."""
class BillingValidationError(BillingDomainError):
    """Billing domain validation failed."""
__all__ = ["BillingConfigurationError", "BillingDomainError", "BillingIntegrityError", "BillingNotFoundError", "BillingPermissionError", "BillingStateError", "BillingValidationError"]
''',
    "apps/billing/foundation/validators.py": '''
"""Shared Billing validation helpers."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from typing import Any
from .currency import normalize_currency
from .exceptions import BillingValidationError
def validate_currency(currency: str) -> str:
    """Validate and normalize a currency code."""
    try:
        return normalize_currency(currency)
    except ValueError as exc:
        raise BillingValidationError(str(exc)) from exc
def validate_money_amount(value: Any, *, field_name: str = "amount", allow_zero: bool = True) -> Decimal:
    """Validate a finite non-negative Decimal amount."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise BillingValidationError(f"{field_name} must be a valid decimal amount.") from exc
    if not amount.is_finite() or amount < Decimal("0"):
        raise BillingValidationError(f"{field_name} must be finite and non-negative.")
    if not allow_zero and amount == Decimal("0"):
        raise BillingValidationError(f"{field_name} must be greater than zero.")
    return amount
def validate_positive_quantity(value: Any, *, field_name: str = "quantity") -> int:
    """Validate a positive integer quantity."""
    if isinstance(value, bool):
        raise BillingValidationError(f"{field_name} must be a positive integer.")
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise BillingValidationError(f"{field_name} must be a positive integer.") from exc
    if quantity <= 0:
        raise BillingValidationError(f"{field_name} must be a positive integer.")
    return quantity
__all__ = ["validate_currency", "validate_money_amount", "validate_positive_quantity"]
''',
    "apps/billing/foundation/status.py": '''
"""Shared Billing lifecycle statuses."""
from __future__ import annotations
from django.db import models
class FinancialDocumentStatus(models.TextChoices):
    """Generic financial document lifecycle."""
    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    VOID = "void", "Void"
    CANCELLED = "cancelled", "Cancelled"
class FinancialTransactionStatus(models.TextChoices):
    """Generic financial transaction lifecycle."""
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REVERSED = "reversed", "Reversed"
    REFUNDED = "refunded", "Refunded"
class ClaimStatus(models.TextChoices):
    """Healthcare insurance claim lifecycle."""
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    APPEALED = "appealed", "Appealed"
    SETTLED = "settled", "Settled"
__all__ = ["ClaimStatus", "FinancialDocumentStatus", "FinancialTransactionStatus"]
''',
    "apps/billing/foundation/permissions.py": '''
"""Canonical explicit Billing permission codes."""
from __future__ import annotations
class BillingPermission:
    """Stable permission codes resolved by platform RBAC."""
    VIEW = "billing.view"
    CREATE = "billing.create"
    UPDATE = "billing.update"
    DELETE = "billing.delete"
    RESTORE = "billing.restore"
    ACTIVATE = "billing.activate"
    DEACTIVATE = "billing.deactivate"
    INVOICE_VIEW = "billing.invoice.view"
    INVOICE_CREATE = "billing.invoice.create"
    INVOICE_UPDATE = "billing.invoice.update"
    INVOICE_DELETE = "billing.invoice.delete"
    INVOICE_VOID = "billing.invoice.void"
    PAYMENT_VIEW = "billing.payment.view"
    PAYMENT_CREATE = "billing.payment.create"
    PAYMENT_REFUND = "billing.payment.refund"
    CLAIM_VIEW = "billing.claim.view"
    CLAIM_CREATE = "billing.claim.create"
    CLAIM_UPDATE = "billing.claim.update"
    CLAIM_APPROVE = "billing.claim.approve"
    CLAIM_REJECT = "billing.claim.reject"
    CLAIM_APPEAL = "billing.claim.appeal"
    CLAIM_SETTLE = "billing.claim.settle"
__all__ = ["BillingPermission"]
''',
    "apps/billing/foundation/rbac.py": '''
"""Billing adapter for the canonical platform RBAC engine."""
from __future__ import annotations
from typing import Any
from apps.platform.rbac.engines import user_has_permission
from .exceptions import BillingPermissionError
def require_billing_permission(*, user: Any, permission: str, organization: Any) -> None:
    """Require an exact Billing permission through platform RBAC."""
    if not user_has_permission(user=user, permission=permission, organization=organization):
        raise BillingPermissionError(f"Missing Billing permission: {permission}")
__all__ = ["require_billing_permission"]
''',
    "apps/billing/foundation/tenant.py": '''
"""Billing tenant and organization boundary helpers."""
from __future__ import annotations
from typing import Any
from apps.platform.organizations.models import Organization
from .exceptions import BillingPermissionError
def require_billing_tenant(request: Any) -> Any:
    """Require an explicit tenant context."""
    tenant = getattr(request, "tenant", None)
    if tenant is None:
        raise BillingPermissionError("Billing requires an explicit tenant context.")
    return tenant
def require_billing_organization(request: Any) -> Organization:
    """Require an explicit organization belonging to the active tenant."""
    tenant = require_billing_tenant(request)
    organization = getattr(request, "organization", None)
    if organization is None:
        raise BillingPermissionError("Billing requires an explicit organization context.")
    if organization.tenant_id != tenant.id:
        raise BillingPermissionError("Organization does not belong to the active tenant.")
    return organization
__all__ = ["require_billing_organization", "require_billing_tenant"]
''',
    "apps/billing/foundation/idempotency.py": '''
"""Idempotency primitives for financial operations."""
from __future__ import annotations
import hashlib
def normalize_idempotency_key(value: str) -> str:
    """Normalize an external idempotency key."""
    normalized = value.strip()
    if not normalized:
        raise ValueError("Idempotency key cannot be empty.")
    return normalized
def idempotency_fingerprint(*, operation: str, key: str) -> str:
    """Create a stable operation/key fingerprint."""
    payload = f"{operation.strip()}:{normalize_idempotency_key(key)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
__all__ = ["idempotency_fingerprint", "normalize_idempotency_key"]
''',
    "apps/billing/foundation/audit.py": '''
"""Billing audit actor primitive."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True, slots=True)
class AuditActor:
    """Identify the user and organization responsible for an operation."""
    user_id: Any
    organization_id: Any
__all__ = ["AuditActor"]
''',
    "apps/billing/foundation/tests/__init__.py": '''"""Billing Foundation test package."""\n\nfrom __future__ import annotations\n\n__all__ = []\n''',
    "apps/billing/foundation/tests/test_money.py": '''
"""Tests for Billing money."""
from __future__ import annotations
from decimal import Decimal
from django.test import SimpleTestCase
from apps.billing.foundation.money import Money
class MoneyTests(SimpleTestCase):
    """Verify Decimal money arithmetic."""
    def test_addition(self) -> None:
        """Add same-currency amounts."""
        self.assertEqual(Money(Decimal("10")).add(Money(Decimal("2"))).amount, Decimal("12"))
    def test_mixed_currency_rejected(self) -> None:
        """Reject mixed-currency arithmetic."""
        with self.assertRaises(ValueError):
            Money(Decimal("10"), "INR").add(Money(Decimal("10"), "USD"))
__all__ = ["MoneyTests"]
''',
    "apps/billing/foundation/tests/test_validators.py": '''
"""Tests for Billing validators."""
from __future__ import annotations
from decimal import Decimal
from django.test import SimpleTestCase
from apps.billing.foundation.exceptions import BillingValidationError
from apps.billing.foundation.validators import validate_money_amount, validate_positive_quantity
class BillingValidatorTests(SimpleTestCase):
    """Verify shared validation rules."""
    def test_money_amount(self) -> None:
        """Return Decimal for valid amounts."""
        self.assertEqual(validate_money_amount("125.50"), Decimal("125.50"))
    def test_negative_rejected(self) -> None:
        """Reject negative amounts."""
        with self.assertRaises(BillingValidationError):
            validate_money_amount("-1")
    def test_zero_can_be_disallowed(self) -> None:
        """Reject zero when positive is required."""
        with self.assertRaises(BillingValidationError):
            validate_money_amount("0", allow_zero=False)
    def test_quantity_must_be_positive(self) -> None:
        """Reject non-positive quantity."""
        with self.assertRaises(BillingValidationError):
            validate_positive_quantity(0)
__all__ = ["BillingValidatorTests"]
''',
    "apps/billing/foundation/tests/test_permissions.py": '''
"""Tests for Billing RBAC delegation."""
from __future__ import annotations
from unittest.mock import patch
from django.test import SimpleTestCase
from apps.billing.foundation.exceptions import BillingPermissionError
from apps.billing.foundation.permissions import BillingPermission
from apps.billing.foundation.rbac import require_billing_permission
class BillingPermissionTests(SimpleTestCase):
    """Verify canonical RBAC delegation."""
    @patch("apps.billing.foundation.rbac.user_has_permission", return_value=True)
    def test_delegates_to_platform_rbac(self, mock_permission) -> None:
        """Delegate exact permission checks."""
        user = object()
        organization = object()
        require_billing_permission(user=user, permission=BillingPermission.INVOICE_VIEW, organization=organization)
        mock_permission.assert_called_once_with(user=user, permission=BillingPermission.INVOICE_VIEW, organization=organization)
    @patch("apps.billing.foundation.rbac.user_has_permission", return_value=False)
    def test_denial_raises(self, mock_permission) -> None:
        """Raise a Billing permission error on denial."""
        with self.assertRaises(BillingPermissionError):
            require_billing_permission(user=object(), permission=BillingPermission.INVOICE_VIEW, organization=object())
__all__ = ["BillingPermissionTests"]
''',
}


def write_sources() -> None:
    """Write all foundation sources."""
    for filename, source in SOURCES.items():
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(source).lstrip(), encoding="utf-8")


def validate() -> None:
    """Validate architecture and compile installed sources."""
    forbidden_patient = "apps.clinical" + ".patients"
    forbidden_rbac = "apps.common.permissions.base import BasePermission"
    for filename, source in SOURCES.items():
        if filename.endswith("test_architecture.py"):
            continue
        if forbidden_patient in source:
            raise RuntimeError("Forbidden dependency: legacy Patient module")
        if forbidden_rbac in source:
            raise RuntimeError("Forbidden legacy RBAC dependency")
    for filename in SOURCES:
        path = Path(filename)
        if not path.exists():
            raise RuntimeError(f"Missing installed file: {path}")
        source = path.read_text(encoding="utf-8")
        if not source.startswith('"""'):
            raise RuntimeError(f"Missing module docstring: {path}")
        if "from __future__ import annotations" not in source:
            raise RuntimeError(f"Missing future annotations: {path}")
        py_compile.compile(str(path), doraise=True)


def main() -> int:
    """Install and validate Billing Foundation."""
    print("=" * 60)
    print("DATAVIONOS — BILLING FOUNDATION INSTALLER")
    print(f"VERSION: {VERSION}")
    print("=" * 60)
    write_sources()
    validate()
    print("MANIFEST: PASS")
    print(f"STYLE: PASS ({len(SOURCES)} Python files)")
    print(f"PY_COMPILE: PASS ({len(SOURCES)} Python files)")
    print("ARCHITECTURE: PASS")
    print("MODELS: NOT MODIFIED")
    print("MIGRATIONS: NOT GENERATED")
    print("LEGACY PATIENT MODULE: NOT MODIFIED")
    print("BILLING FOUNDATION INSTALLATION COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
