"""Tenant-safe claim submission selectors."""

from __future__ import annotations

from apps.revenue_cycle.claim_submission.models import ClaimSubmission


def list_submissions(*, organization):
    """Return active submissions for an organization."""

    return ClaimSubmission.objects.filter(organization=organization).select_related(
        "patient", "created_by"
    )


def get_submission(*, organization, submission_id):
    """Return one active submission within the organization."""

    return ClaimSubmission.objects.select_related("patient", "created_by").get(
        organization=organization,
        id=submission_id,
    )


def get_submission_for_update(*, organization, submission_id):
    """Return one submission with a row lock for mutation."""

    return (
        ClaimSubmission.objects.select_for_update()
        .select_related("patient")
        .get(
            organization=organization,
            id=submission_id,
        )
    )


def get_by_idempotency_key(*, organization, idempotency_key):
    """Return an existing submission by its organization-scoped idempotency key."""

    return ClaimSubmission.objects.filter(
        organization=organization,
        idempotency_key=idempotency_key,
    ).first()


def get_deleted_submission_for_update(*, organization, submission_id):
    """Return a deleted submission with a row lock for restoration."""

    return ClaimSubmission.all_objects.select_for_update().get(
        organization=organization,
        id=submission_id,
        is_deleted=True,
    )


__all__ = (
    "list_submissions",
    "get_submission",
    "get_submission_for_update",
    "get_by_idempotency_key",
    "get_deleted_submission_for_update",
)
