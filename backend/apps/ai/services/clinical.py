"""Clinician-controlled AI workflows with immutable versions."""

from __future__ import annotations

from django.db import transaction

from apps.ai.models import AIClinicalArtifact, AIClinicalArtifactVersion, AIDoctorReview
from apps.ai.services.rbac import (
    AI_CREATE,
    AI_SIGN,
    AI_UPDATE,
    AI_VERIFY,
    require_ai_permission,
)


def create_artifact(
    *,
    user,
    tenant,
    organization,
    application,
    module_reference,
    artifact_type,
    source_content,
    normalized_content="",
    structured_content=None,
    ai_metadata=None,
):
    require_ai_permission(user=user, organization=organization, permission=AI_CREATE)
    if (
        module_reference.tenant_id != tenant.id
        or module_reference.organization_id != organization.id
    ):
        raise ValueError("Module reference scope mismatch.")
    with transaction.atomic():
        artifact = AIClinicalArtifact.objects.create(
            tenant=tenant,
            organization=organization,
            application=application,
            module_reference=module_reference,
            artifact_type=artifact_type,
            status=AIClinicalArtifact.PENDING_REVIEW,
            current_version=1,
            created_by=user,
        )
        AIClinicalArtifactVersion.objects.create(
            artifact=artifact,
            version_number=1,
            source_content=source_content,
            normalized_content=normalized_content,
            structured_content=structured_content or {},
            ai_metadata=ai_metadata or {},
            created_by=user,
        )
    return artifact


def create_new_version(
    *,
    user,
    organization,
    artifact,
    source_content="",
    normalized_content="",
    structured_content=None,
    ai_metadata=None,
):
    require_ai_permission(user=user, organization=organization, permission=AI_UPDATE)
    if artifact.organization_id != organization.id:
        raise ValueError("Artifact is outside organization scope.")
    with transaction.atomic():
        next_version = artifact.current_version + 1
        version = AIClinicalArtifactVersion.objects.create(
            artifact=artifact,
            version_number=next_version,
            source_content=source_content,
            normalized_content=normalized_content,
            structured_content=structured_content or {},
            ai_metadata=ai_metadata or {},
            created_by=user,
        )
        artifact.current_version = next_version
        artifact.status = AIClinicalArtifact.PENDING_REVIEW
        artifact.save(update_fields=("current_version", "status", "updated_at"))
    return version


def review_artifact(
    *, user, organization, artifact_version, action, comments="", signature_reference=""
):
    permission = (
        AI_SIGN
        if action == AIDoctorReview.SIGN
        else AI_VERIFY
        if action == AIDoctorReview.VERIFY
        else AI_UPDATE
    )
    require_ai_permission(user=user, organization=organization, permission=permission)
    artifact = artifact_version.artifact
    if artifact.organization_id != organization.id:
        raise ValueError("Artifact is outside organization scope.")
    if (
        action == AIDoctorReview.VERIFY
        and artifact.status != AIClinicalArtifact.PENDING_REVIEW
    ):
        raise ValueError("Only pending-review artifacts can be verified.")
    if action == AIDoctorReview.SIGN and artifact.status != AIClinicalArtifact.VERIFIED:
        raise ValueError("Artifact must be verified before signing.")
    if action == AIDoctorReview.SIGN and not signature_reference.strip():
        raise ValueError("Doctor signature reference is required for signing.")
    with transaction.atomic():
        AIDoctorReview.objects.create(
            artifact_version=artifact_version,
            doctor=user,
            action=action,
            comments=comments,
            signature_reference=signature_reference,
        )
        artifact.status = {
            AIDoctorReview.VERIFY: AIClinicalArtifact.VERIFIED,
            AIDoctorReview.SIGN: AIClinicalArtifact.SIGNED,
            AIDoctorReview.REJECT: AIClinicalArtifact.REJECTED,
        }[action]
        artifact.save(update_fields=("status", "updated_at"))
    return artifact


__all__ = ("create_artifact", "create_new_version", "review_artifact")
