"""Clinical AI safety and versioning contracts."""

from __future__ import annotations

from apps.ai.models import (
    AIClinicalArtifact,
    AIClinicalArtifactVersion,
    AIDoctorReview,
    AIModuleReference,
)


def test_clinical_artifact_contract():
    assert AIClinicalArtifact._meta.get_field("module_reference").null is False
    assert AIClinicalArtifactVersion._meta.get_field("version_number").null is False
    assert AIDoctorReview._meta.get_field("doctor").null is False
    assert AIModuleReference._meta.get_field("module_code").null is False


def test_signature_state_contract():
    assert AIClinicalArtifact.PENDING_REVIEW != AIClinicalArtifact.VERIFIED
    assert AIClinicalArtifact.VERIFIED != AIClinicalArtifact.SIGNED
