"""Architecture tests for Patient Documents."""

from __future__ import annotations

from pathlib import Path

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


def test_canonical_patient_model_is_used() -> None:
    """Ensure PatientDocument points to the canonical Patient model."""
    from apps.patient_management.patients.models import Patient

    assert (
        PatientDocument._meta.get_field(
            "patient",
        ).remote_field.model
        is Patient
    )


def test_patient_document_does_not_define_a_duplicate_patient_model() -> None:
    """Ensure the bounded context uses the canonical Patient module."""
    assert (
        PatientDocument._meta.get_field(
            "patient",
        ).remote_field.model.__module__
        == "apps.patient_management.patients.models"
    )


def test_access_audit_is_workflow_orchestrated() -> None:
    """Ensure the API does not directly invoke the access-log service."""
    views_source = Path(__file__).resolve().parents[1] / "api" / "views.py"
    source = views_source.read_text(encoding="utf-8")
    assert "PatientDocumentAccessLogService.record(" not in source
    assert "PatientDocumentAccessWorkflow(" in source


def test_version_creation_is_workflow_orchestrated() -> None:
    """Ensure the API does not directly invoke the version service."""
    views_source = Path(__file__).resolve().parents[1] / "api" / "views.py"
    source = views_source.read_text(encoding="utf-8")
    assert "PatientDocumentVersionService.create(" not in source
    assert "PatientDocumentVersionCreationWorkflow(" in source


def test_lifecycle_and_access_routes_exist() -> None:
    """Ensure lifecycle and access operations expose explicit API routes."""
    urls_source = Path(__file__).resolve().parents[1] / "api" / "urls.py"
    source = urls_source.read_text(encoding="utf-8")
    assert 'name="activate"' in source
    assert 'name="access-audit"' in source


__all__: tuple[str, ...] = ()
