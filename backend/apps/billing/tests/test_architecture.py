"""
Billing Core architecture tests.
"""

from __future__ import annotations

from pathlib import Path

from apps.billing.models import InsuranceClaim, Invoice, Payment


def test_canonical_patient_relations() -> None:
    """All Billing Core patient relations use canonical Patient."""
    fields = (
        Invoice._meta.get_field("patient"),
        Payment._meta.get_field("patient"),
        InsuranceClaim._meta.get_field("patient"),
    )

    for field in fields:
        assert field.remote_field.model._meta.label == "patient_core.Patient"


def test_no_legacy_patient_imports() -> None:
    """Billing Core must not reference the legacy Patient package."""
    root = Path(__file__).resolve().parents[1]

    for path in root.rglob("*.py"):
        text = path.read_text(
            encoding="utf-8",
        )
        assert "apps.clinical.patients" not in text


def test_workflow_registry() -> None:
    """Billing Core mutation workflows are registered."""
    from apps.billing.workflow_registry import register_billing_workflows
    from apps.core.workflows import workflow_registry

    register_billing_workflows()

    for name in (
        "billing.invoice.create",
        "billing.payment.create",
        "billing.claim.approve",
    ):
        assert workflow_registry.is_registered(name)


__all__ = (
    "test_canonical_patient_relations",
    "test_no_legacy_patient_imports",
    "test_workflow_registry",
)
