"""Constants for Revenue Cycle cross-module integration."""

from __future__ import annotations

from django.db import models


class IntegrationRecordStatus(models.TextChoices):
    """Supported integration record states."""

    PENDING = "PENDING", "Pending"
    PROCESSED = "PROCESSED", "Processed"
    FAILED = "FAILED", "Failed"
    IGNORED = "IGNORED", "Ignored"


class IntegrationSource(models.TextChoices):
    """Supported Revenue Cycle source contexts."""

    ELIGIBILITY = "ELIGIBILITY", "Eligibility"
    INSURANCE_VERIFICATION = "INSURANCE_VERIFICATION", "Insurance Verification"
    PRIOR_AUTHORIZATION = "PRIOR_AUTHORIZATION", "Prior Authorization"
    CHARGE_CAPTURE = "CHARGE_CAPTURE", "Charge Capture"
    CODING = "CODING", "Coding"
    CLAIM_SCRUBBING = "CLAIM_SCRUBBING", "Claim Scrubbing"
    CLAIM_SUBMISSION = "CLAIM_SUBMISSION", "Claim Submission"
    PAYMENT_POSTING = "PAYMENT_POSTING", "Payment Posting"
    ERA = "ERA", "ERA"
    DENIALS = "DENIALS", "Denials"
    APPEALS = "APPEALS", "Appeals"
    ACCOUNTS_RECEIVABLE = "ACCOUNTS_RECEIVABLE", "Accounts Receivable"
    REVENUE_ANALYTICS = "REVENUE_ANALYTICS", "Revenue Analytics"


class IntegrationEventType(models.TextChoices):
    """Supported integration event categories."""

    PATIENT_CONTEXT = "PATIENT_CONTEXT", "Patient Context"
    CLAIM_CONTEXT = "CLAIM_CONTEXT", "Claim Context"
    PAYMENT_CONTEXT = "PAYMENT_CONTEXT", "Payment Context"
    AR_CONTEXT = "AR_CONTEXT", "AR Context"
    ANALYTICS_CONTEXT = "ANALYTICS_CONTEXT", "Analytics Context"


__all__ = (
    "IntegrationEventType",
    "IntegrationRecordStatus",
    "IntegrationSource",
)
