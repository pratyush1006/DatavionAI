"""
Domain exceptions and workflow failure helpers for Patient Referrals.
"""

from __future__ import annotations

from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class ReferralError(Exception):
    """Base exception for referral domain failures."""


class ReferralValidationError(ReferralError):
    """Raised when referral data violates domain rules."""


class ReferralNotFoundError(ReferralError):
    """Raised when a referral cannot be found in the tenant boundary."""


class ReferralTransitionError(ReferralError):
    """Raised when an invalid referral lifecycle transition is requested."""


def referral_failure_result(
    *,
    context: Any,
    exception: Exception,
):
    """Build a deterministic failed workflow result for expected domain errors."""

    from apps.core.workflows import WorkflowResult

    if isinstance(exception, PermissionError):
        code = "patient_referral_permission_denied"
    elif isinstance(exception, (ReferralNotFoundError, ObjectDoesNotExist)):
        code = "patient_referral_not_found"
    elif isinstance(exception, ReferralTransitionError):
        code = "patient_referral_invalid_transition"
    elif isinstance(exception, ReferralValidationError):
        code = "patient_referral_validation_error"
    elif isinstance(exception, IntegrityError):
        code = "patient_referral_duplicate_number"
    else:
        code = "workflow_execution_error"

    return WorkflowResult.fail(
        context=context,
        message=str(exception),
        code=code,
    )


__all__ = (
    "ReferralError",
    "ReferralNotFoundError",
    "ReferralTransitionError",
    "ReferralValidationError",
    "referral_failure_result",
)
