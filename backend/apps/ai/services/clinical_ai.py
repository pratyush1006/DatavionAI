"""AI-assisted clinical note cleaning and prescription drafting."""

from __future__ import annotations

from apps.ai.models import AIClinicalArtifact
from apps.ai.services.chat import generate
from apps.ai.services.clinical import create_artifact
from apps.ai.services.rbac import AI_CREATE, require_ai_permission


def clean_clinical_note(
    *,
    user,
    tenant,
    organization,
    application,
    module_reference,
    raw_note: str,
    model="gpt-4o-mini",
    provider_name=None,
):
    require_ai_permission(user=user, organization=organization, permission=AI_CREATE)
    if module_reference.module_code != "notes":
        raise ValueError(
            "Clinical note cleaning requires the canonical notes module reference."
        )
    prompt = (
        "Clean and normalize this clinical note. Remove transcription noise, filler, repetition and irrelevant speech. "
        "Do not invent, infer, diagnose or change clinical facts. Preserve uncertainty explicitly. Return only the cleaned note.\n\n"
        + raw_note
    )
    result = generate(
        application=application,
        tenant=tenant,
        organization=organization,
        module_reference=module_reference,
        provider_name=provider_name,
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=4096,
    )
    return create_artifact(
        user=user,
        tenant=tenant,
        organization=organization,
        application=application,
        module_reference=module_reference,
        artifact_type=AIClinicalArtifact.NOTE_CLEANING,
        source_content=raw_note,
        normalized_content=result.content,
        ai_metadata={"provider": result.provider, "model": result.model},
    )


def draft_prescription(
    *,
    user,
    tenant,
    organization,
    application,
    module_reference,
    clinical_context: str,
    model="gpt-4o-mini",
    provider_name=None,
):
    require_ai_permission(user=user, organization=organization, permission=AI_CREATE)
    if module_reference.module_code != "clinical.prescriptions":
        raise ValueError(
            "Prescription drafting requires the canonical clinical.prescriptions module reference."
        )
    prompt = (
        "Create a clinician-reviewable prescription draft from the supplied clinical context. "
        "Do not claim that a prescription has been issued. Do not invent missing patient facts, allergies, diagnoses, doses or contraindications. "
        "If information is insufficient, state what is missing. Return a structured draft with medication, dose, route, frequency, duration and rationale where supported.\n\n"
        + clinical_context
    )
    result = generate(
        application=application,
        tenant=tenant,
        organization=organization,
        module_reference=module_reference,
        provider_name=provider_name,
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=4096,
    )
    return create_artifact(
        user=user,
        tenant=tenant,
        organization=organization,
        application=application,
        module_reference=module_reference,
        artifact_type=AIClinicalArtifact.PRESCRIPTION_DRAFT,
        source_content=clinical_context,
        normalized_content=result.content,
        ai_metadata={
            "provider": result.provider,
            "model": result.model,
            "requires_doctor_verification": True,
            "requires_doctor_signature": True,
        },
    )


__all__ = ("clean_clinical_note", "draft_prescription")
