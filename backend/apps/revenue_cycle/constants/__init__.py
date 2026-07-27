"""
Shared constants for the Revenue Cycle Management application.
"""

from __future__ import annotations

from django.db import models


class VerificationStatus(models.TextChoices):
    """
    Insurance verification outcome.
    """

    VERIFIED = "verified", "Verified"

    NOT_VERIFIED = "not_verified", "Not Verified"

    PENDING = "pending", "Pending"

    FAILED = "failed", "Failed"


class EligibilityStatus(models.TextChoices):
    """
    Eligibility check outcome.
    """

    ELIGIBLE = "eligible", "Eligible"

    NOT_ELIGIBLE = "not_eligible", "Not Eligible"

    PENDING = "pending", "Pending"

    UNKNOWN = "unknown", "Unknown"


class CodeSystem(models.TextChoices):
    """
    Clinical / billing code systems.
    """

    ICD10 = "icd10", "ICD-10"

    CPT = "cpt", "CPT"

    HCPCS = "hcpcs", "HCPCS"

    SNOMED = "snomed", "SNOMED CT"

    LOINC = "loinc", "LOINC"

    NDCS = "ndc", "NDC"


class ClaimPriority(models.TextChoices):
    """
    Claim submission priority.
    """

    NORMAL = "normal", "Normal"

    HIGH = "high", "High"


class SubmissionMethod(models.TextChoices):
    """
    Electronic vs manual claim submission.
    """

    ELECTRONIC = "electronic", "Electronic"

    PAPER = "paper", "Paper"

    CLEARINGHOUSE = "clearinghouse", "Clearinghouse"


class ScrubResult(models.TextChoices):
    """
    Claim scrubbing outcome.
    """

    PASSED = "passed", "Passed"

    FAILED = "failed", "Failed"

    WARNING = "warning", "Warning"


class RemittanceType(models.TextChoices):
    """
    ERA remittance advice type.
    """

    PAYMENT = "payment", "Payment"

    ADJUSTMENT = "adjustment", "Adjustment"

    DENIAL = "denial", "Denial"


class PostingStatus(models.TextChoices):
    """
    Payment posting status.
    """

    POSTED = "posted", "Posted"

    PENDING = "pending", "Pending"

    REVERSED = "reversed", "Reversed"


class DenialReason(models.TextChoices):
    """
    Common claim denial reasons.
    """

    MISSING_INFO = "missing_info", "Missing Information"

    NOT_COVERED = "not_covered", "Service Not Covered"

    DUPLICATE = "duplicate", "Duplicate Claim"

    AUTHORIZATION = "authorization", "Prior Auth Required"

    ELIGIBILITY = "eligibility", "Eligibility Issue"

    CODING = "coding", "Coding Error"

    OTHER = "other", "Other"


class AppealStatus(models.TextChoices):
    """
    Appeal lifecycle status.
    """

    DRAFT = "draft", "Draft"

    SUBMITTED = "submitted", "Submitted"

    UNDER_REVIEW = "under_review", "Under Review"

    WON = "won", "Won"

    LOST = "lost", "Lost"

    WITHDRAWN = "withdrawn", "Withdrawn"


class ArStatus(models.TextChoices):
    """
    Accounts receivable bucket status.
    """

    CURRENT = "current", "Current"

    AGING_30 = "aging_30", "31-60 Days"

    AGING_60 = "aging_60", "61-90 Days"

    AGING_90 = "aging_90", "90+ Days"

    COLLECTIONS = "collections", "Collections"

    PAID = "paid", "Paid"

    WRITTEN_OFF = "written_off", "Written Off"


class BatchStatus(models.TextChoices):
    """
    Billing batch status.
    """

    OPEN = "open", "Open"

    CLOSED = "closed", "Closed"

    SUBMITTED = "submitted", "Submitted"


class MetricCategory(models.TextChoices):
    """
    RCM analytics metric category.
    """

    REVENUE = "revenue", "Revenue"

    DENIAL = "denial", "Denial"

    AR = "ar", "Accounts Receivable"

    COLLECTION = "collection", "Collection"

    PRODUCTIVITY = "productivity", "Productivity"


__all__ = [
    "AppealStatus",
    "ArStatus",
    "BatchStatus",
    "ClaimPriority",
    "CodeSystem",
    "DenialReason",
    "EligibilityStatus",
    "MetricCategory",
    "PostingStatus",
    "RemittanceType",
    "ScrubResult",
    "SubmissionMethod",
    "VerificationStatus",
]
