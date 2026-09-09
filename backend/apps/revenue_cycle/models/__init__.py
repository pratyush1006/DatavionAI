"""
Revenue Cycle aggregate model exports.

This module imports every concrete Revenue Cycle model so Django
discovers the complete Revenue Cycle model graph when the
``apps.revenue_cycle`` application is loaded.

Each bounded context remains the canonical owner of its models.
This module exists only as the aggregate discovery and export
surface for the Revenue Cycle Django application.
"""

from __future__ import annotations

from apps.revenue_cycle.accounts_receivable.models import (
    ARAccount,
    ARActivityLog,
    ARTransaction,
)
from apps.revenue_cycle.appeals.models import Appeal
from apps.revenue_cycle.charge_capture.models import Charge
from apps.revenue_cycle.claim_scrubbing.models import (
    ClaimScrub,
    ClaimScrubFinding,
    ScrubRule,
)
from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from apps.revenue_cycle.coding.models import CodeAssignment, CodingRecord
from apps.revenue_cycle.cross_module_integration.models import (
    RevenueCycleIntegrationRecord,
)
from apps.revenue_cycle.denials.models import Denial
from apps.revenue_cycle.eligibility.models import Eligibility
from apps.revenue_cycle.era.models import ERA
from apps.revenue_cycle.insurance_verification.models import InsuranceVerification
from apps.revenue_cycle.payment_posting.models import PaymentPosting
from apps.revenue_cycle.prior_authorization.models import PriorAuthorization
from apps.revenue_cycle.revenue_analytics.models import RevenueMetricSnapshot

__all__ = (
    "ARAccount",
    "ARActivityLog",
    "ARTransaction",
    "Appeal",
    "Charge",
    "ClaimScrub",
    "ClaimScrubFinding",
    "ScrubRule",
    "ClaimSubmission",
    "CodeAssignment",
    "CodingRecord",
    "RevenueCycleIntegrationRecord",
    "Denial",
    "Eligibility",
    "ERA",
    "InsuranceVerification",
    "PaymentPosting",
    "PriorAuthorization",
    "RevenueMetricSnapshot",
)
