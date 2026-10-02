"""Workflow orchestration for claim submission."""

from __future__ import annotations

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.claim_submission.services import (
    create_submission,
    delete_submission,
    restore_submission,
    transition_submission,
    update_submission,
)


def _organization(request):
    """Resolve the organization for a workflow command."""

    return Organization.objects.get(
        id=request.organization_id, tenant_id=request.tenant_id
    )


def _user(request):
    """Resolve the acting user for a workflow command."""

    from django.contrib.auth import get_user_model

    return get_user_model().objects.get(id=request.user_id)


class CreateClaimSubmissionWorkflow(BaseWorkflow):
    """Create a claim submission."""

    def _run(self, context: WorkflowContext):
        request = context.payload
        organization = _organization(request)
        user = _user(request)
        patient = Patient.objects.get(id=request.patient_id, organization=organization)
        submission, created = create_submission(
            organization=organization,
            patient=patient,
            user=user,
            claim_reference=request.claim_reference,
            payer_id=request.payer_id,
            payer_name=request.payer_name,
            submission_method=request.submission_method,
            idempotency_key=request.idempotency_key,
            payload=request.payload,
        )
        return WorkflowResult.ok(
            context=context, data=submission, metadata={"created": created}
        )


class UpdateClaimSubmissionWorkflow(BaseWorkflow):
    """Update a claim submission."""

    def _run(self, context: WorkflowContext):
        request = context.payload
        submission = update_submission(
            organization=_organization(request),
            submission_id=request.submission_id,
            user=_user(request),
            changes=request.changes,
        )
        return WorkflowResult.ok(context=context, data=submission)


class TransitionClaimSubmissionWorkflow(BaseWorkflow):
    """Transition a claim submission lifecycle state."""

    def _run(self, context: WorkflowContext):
        request = context.payload
        submission = transition_submission(
            organization=_organization(request),
            submission_id=request.submission_id,
            target_status=request.target_status,
            user=_user(request),
            response_data=request.response_data,
            external_submission_id=request.external_submission_id,
            rejection_code=request.rejection_code,
            rejection_reason=request.rejection_reason,
        )
        return WorkflowResult.ok(context=context, data=submission)


class DeleteClaimSubmissionWorkflow(BaseWorkflow):
    """Soft-delete a claim submission."""

    def _run(self, context: WorkflowContext):
        request = context.payload
        submission = delete_submission(
            organization=_organization(request),
            submission_id=request.submission_id,
            user=_user(request),
        )
        return WorkflowResult.ok(context=context, data=submission)


class RestoreClaimSubmissionWorkflow(BaseWorkflow):
    """Restore a deleted claim submission."""

    def _run(self, context: WorkflowContext):
        request = context.payload
        submission = restore_submission(
            organization=_organization(request),
            submission_id=request.submission_id,
            user=_user(request),
        )
        return WorkflowResult.ok(context=context, data=submission)


__all__ = (
    "CreateClaimSubmissionWorkflow",
    "UpdateClaimSubmissionWorkflow",
    "TransitionClaimSubmissionWorkflow",
    "DeleteClaimSubmissionWorkflow",
    "RestoreClaimSubmissionWorkflow",
)
