"""Transactional Denial domain services."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .constants import DENIAL_TRANSITIONS, DenialStatus
from .exceptions import InvalidDenialTransition
from .models import Denial
from .selectors import get_deleted_denial_for_update, get_denial_for_update


def _validate_transition(*, current: str, target: str) -> None:
    """Validate a governed lifecycle transition."""
    if target not in DENIAL_TRANSITIONS.get(current, set()):
        raise InvalidDenialTransition(
            f"Cannot transition denial from {current!r} to {target!r}."
        )


@transaction.atomic
def create_denial(*, organization, patient, actor, data: dict) -> Denial:
    """Create a denial atomically."""
    return Denial.objects.create(
        organization=organization, patient=patient, created_by=actor, **data
    )


@transaction.atomic
def update_denial(*, denial: Denial, data: dict) -> Denial:
    """Update mutable denial fields under a row lock."""
    locked = get_denial_for_update(
        organization_id=denial.organization_id,
        tenant_id=denial.organization.tenant_id,
        denial_id=denial.id,
    )
    for field, value in data.items():
        setattr(locked, field, value)
    locked.save()
    return locked


@transaction.atomic
def transition_denial(
    *, denial: Denial, target_status: str, resolution_note: str = ""
) -> Denial:
    """Transition a denial under a row lock."""
    locked = get_denial_for_update(
        organization_id=denial.organization_id,
        tenant_id=denial.organization.tenant_id,
        denial_id=denial.id,
    )
    _validate_transition(current=locked.status, target=target_status)
    locked.status = target_status
    if resolution_note:
        locked.resolution_note = resolution_note
    if target_status in {DenialStatus.RESOLVED, DenialStatus.WRITTEN_OFF}:
        locked.resolved_at = timezone.now()
    locked.save()
    return locked


@transaction.atomic
def delete_denial(*, denial: Denial, actor_id) -> Denial:
    """Soft-delete a denial under a row lock."""
    locked = get_denial_for_update(
        organization_id=denial.organization_id,
        tenant_id=denial.organization.tenant_id,
        denial_id=denial.id,
    )
    locked.delete(user_id=actor_id)
    return locked


@transaction.atomic
def restore_denial(*, organization_id, tenant_id, denial_id) -> Denial:
    """Restore a deleted denial under a row lock."""
    locked = get_deleted_denial_for_update(
        organization_id=organization_id, tenant_id=tenant_id, denial_id=denial_id
    )
    locked.restore()
    return locked


__all__ = (
    "create_denial",
    "update_denial",
    "transition_denial",
    "delete_denial",
    "restore_denial",
)
