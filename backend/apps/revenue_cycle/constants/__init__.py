"""Shared Revenue Cycle constants."""

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


REVENUE_CYCLE_MODULES = tuple(module.value for module in RevenueCycleModule)

__all__ = (
    "RevenueCycleModule",
    "REVENUE_CYCLE_MODULES",
)
