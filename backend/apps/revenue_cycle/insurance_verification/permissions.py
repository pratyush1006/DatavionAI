"""Revenue Cycle Insurance Verification RBAC permission codes."""

from __future__ import annotations

from enum import StrEnum


class InsuranceVerificationPermission(StrEnum):
    """Exact platform RBAC permission codes."""

    VIEW = "revenue_cycle.insurance_verification.view"
    CREATE = "revenue_cycle.insurance_verification.create"
    UPDATE = "revenue_cycle.insurance_verification.update"
    DELETE = "revenue_cycle.insurance_verification.delete"
    RESTORE = "revenue_cycle.insurance_verification.restore"
    LIFECYCLE = "revenue_cycle.insurance_verification.lifecycle"


__all__ = ("InsuranceVerificationPermission",)
