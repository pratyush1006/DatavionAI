"""Transactional services for claim submission."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.revenue_cycle.claim_submission.constants import SubmissionStatus
from apps.revenue_cycle.claim_submission.events.events import (
    ClaimSubmissionCreated,
    ClaimSubmissionDeleted,
    ClaimSubmissionRestored,
    ClaimSubmissionStatusChanged,
    ClaimSubmissionUpdated,
)
from apps.revenue_cycle.claim_submission.exceptions import (
    InvalidSubmissionTransition,
    SubmissionValidationError,
)
from apps.revenue_cycle.claim_submission.models import ClaimSubmission
from apps.revenue_cycle.claim_submission.selectors import (
    get_by_idempotency_key,
    get_deleted_submission_for_update,
    get_submission_for_update,
)

ALLOWED_TRANSITIONS = {
    SubmissionStatus.PENDING: {SubmissionStatus.VALIDATED, SubmissionStatus.CANCELLED},
    SubmissionStatus.VALIDATED: {
        SubmissionStatus.SUBMITTING,
        SubmissionStatus.CANCELLED,
    },
    SubmissionStatus.SUBMITTING: {SubmissionStatus.SUBMITTED, SubmissionStatus.FAILED},
    SubmissionStatus.SUBMITTED: {
        SubmissionStatus.ACCEPTED,
        SubmissionStatus.REJECTED,
        SubmissionStatus.FAILED,
    },
    SubmissionStatus.ACCEPTED: set(),
    SubmissionStatus.REJECTED: set(),
    SubmissionStatus.FAILED: {SubmissionStatus.PENDING, SubmissionStatus.CANCELLED},
    SubmissionStatus.CANCELLED: set(),
}


def _publish(event):
    """Publish a domain event after the surrounding transaction commits."""

    from apps.core.events.dispatcher import publish_after_commit

    publish_after_commit(event)


def create_submission(
    *,
    organization,
    patient,
    user,
    claim_reference,
    payer_id,
    idempotency_key,
    payload=None,
    payer_name="",
    submission_method="edi",
):
    """Create an idempotent claim submission."""

    with transaction.atomic():
        existing = get_by_idempotency_key(
            organization=organization, idempotency_key=idempotency_key
        )
        if existing is not None:
            return existing, False
        submission = ClaimSubmission.objects.create(
            organization=organization,
            patient=patient,
            claim_reference=claim_reference,
            payer_id=payer_id,
            payer_name=payer_name,
            submission_method=submission_method,
            payload=payload or {},
            idempotency_key=idempotency_key,
            created_by=user,
        )
        _publish(
            ClaimSubmissionCreated(
                submission_id=str(submission.id), organization_id=str(organization.id)
            )
        )
        return submission, True


def update_submission(*, organization, submission_id, user, changes):
    """Update mutable submission metadata under a row lock."""

    with transaction.atomic():
        submission = get_submission_for_update(
            organization=organization, submission_id=submission_id
        )
        if submission.status in {
            SubmissionStatus.SUBMITTING,
            SubmissionStatus.SUBMITTED,
            SubmissionStatus.ACCEPTED,
        }:
            protected = {
                "claim_reference",
                "payer_id",
                "patient_id",
                "submission_method",
                "payload",
            }
            if protected.intersection(changes):
                raise SubmissionValidationError(
                    "Submitted claim data cannot be changed."
                )
        before = {key: getattr(submission, key, None) for key in changes}
        for key, value in changes.items():
            setattr(submission, key, value)
        submission.save(update_fields=list(changes) + ["updated_at"])
        _publish(
            ClaimSubmissionUpdated(
                submission_id=str(submission.id),
                organization_id=str(organization.id),
                changes=before,
            )
        )
        return submission


def transition_submission(
    *,
    organization,
    submission_id,
    target_status,
    user,
    response_data=None,
    external_submission_id="",
    rejection_code="",
    rejection_reason="",
):
    """Transition a submission through its strict lifecycle."""

    with transaction.atomic():
        submission = get_submission_for_update(
            organization=organization, submission_id=submission_id
        )
        allowed = ALLOWED_TRANSITIONS.get(submission.status, set())
        if target_status not in allowed:
            raise InvalidSubmissionTransition(
                f"Cannot transition from {submission.status} to {target_status}."
            )
        previous = submission.status
        submission.status = target_status
        if response_data is not None:
            submission.response_data = response_data
        if external_submission_id:
            submission.external_submission_id = external_submission_id
        if rejection_code:
            submission.rejection_code = rejection_code
        if rejection_reason:
            submission.rejection_reason = rejection_reason
        now = timezone.now()
        if target_status == SubmissionStatus.SUBMITTED:
            submission.submitted_at = now
        if target_status == SubmissionStatus.ACCEPTED:
            submission.accepted_at = now
        if target_status == SubmissionStatus.FAILED:
            submission.failed_at = now
        if target_status == SubmissionStatus.CANCELLED:
            submission.cancelled_at = now
        submission.save()
        _publish(
            ClaimSubmissionStatusChanged(
                submission_id=str(submission.id),
                organization_id=str(organization.id),
                previous_status=previous,
                status=target_status,
            )
        )
        return submission


def delete_submission(*, organization, submission_id, user):
    """Soft-delete a submission under a row lock."""

    with transaction.atomic():
        submission = get_submission_for_update(
            organization=organization, submission_id=submission_id
        )
        if submission.status in {
            SubmissionStatus.SUBMITTING,
            SubmissionStatus.SUBMITTED,
        }:
            raise SubmissionValidationError(
                "An in-flight or submitted claim cannot be deleted."
            )
        submission.delete(user_id=getattr(user, "id", None))
        _publish(
            ClaimSubmissionDeleted(
                submission_id=str(submission.id), organization_id=str(organization.id)
            )
        )
        return submission


def restore_submission(*, organization, submission_id, user):
    """Restore a soft-deleted submission under a row lock."""

    with transaction.atomic():
        submission = get_deleted_submission_for_update(
            organization=organization, submission_id=submission_id
        )
        submission.restore()
        _publish(
            ClaimSubmissionRestored(
                submission_id=str(submission.id), organization_id=str(organization.id)
            )
        )
        return submission


__all__ = (
    "create_submission",
    "update_submission",
    "transition_submission",
    "delete_submission",
    "restore_submission",
    "ALLOWED_TRANSITIONS",
)
