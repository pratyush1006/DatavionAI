"""Transactional ERA domain services."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .constants import ERAStatus
from .exceptions import ERAValidationError, InvalidERATransition
from .models import ERA
from .selectors import get_deleted_era_for_update, get_era_for_update


def validate_era(*, era: ERA) -> ERA:
    """Validate an ERA envelope before posting."""

    if era.status != ERAStatus.RECEIVED:
        raise InvalidERATransition("Only received ERAs can be validated.")
    if not era.payer_name.strip() or not era.trace_number.strip():
        raise ERAValidationError("Payer name and trace number are required.")
    if era.payment_amount < 0 or era.adjustment_amount < 0:
        raise ERAValidationError("ERA monetary values cannot be negative.")
    era.status = ERAStatus.VALIDATED
    era.validated_at = timezone.now()
    era.validation_errors = []
    era.save(
        update_fields=("status", "validated_at", "validation_errors", "updated_at")
    )
    return era


@transaction.atomic
def post_era(*, organization_id, tenant_id, era_id, user) -> ERA:
    """Move a validated ERA into posted state with row locking."""

    era = get_era_for_update(
        organization_id=organization_id, tenant_id=tenant_id, era_id=era_id
    )
    if era.status != ERAStatus.VALIDATED:
        raise InvalidERATransition("Only validated ERAs can be posted.")
    era.status = ERAStatus.POSTED
    era.posted_at = timezone.now()
    era.processed_by = user
    era.save(update_fields=("status", "posted_at", "processed_by", "updated_at"))
    return era


@transaction.atomic
def reverse_era(*, organization_id, tenant_id, era_id, user) -> ERA:
    """Reverse a posted ERA with row locking."""

    era = get_era_for_update(
        organization_id=organization_id, tenant_id=tenant_id, era_id=era_id
    )
    if era.status != ERAStatus.POSTED:
        raise InvalidERATransition("Only posted ERAs can be reversed.")
    era.status = ERAStatus.REVERSED
    era.reversed_at = timezone.now()
    era.processed_by = user
    era.save(update_fields=("status", "reversed_at", "processed_by", "updated_at"))
    return era


@transaction.atomic
def delete_era(*, organization_id, tenant_id, era_id, user_id) -> ERA:
    """Soft-delete an ERA after enforcing lifecycle rules."""

    era = get_era_for_update(
        organization_id=organization_id, tenant_id=tenant_id, era_id=era_id
    )
    if era.status == ERAStatus.POSTED:
        raise InvalidERATransition("Posted ERAs cannot be deleted.")
    era.delete(user_id=user_id)
    return era


@transaction.atomic
def restore_era(*, organization_id, tenant_id, era_id) -> ERA:
    """Restore a deleted ERA with row locking."""

    era = get_deleted_era_for_update(
        organization_id=organization_id, tenant_id=tenant_id, era_id=era_id
    )
    era.restore()
    return era


__all__ = ("delete_era", "post_era", "restore_era", "reverse_era", "validate_era")
