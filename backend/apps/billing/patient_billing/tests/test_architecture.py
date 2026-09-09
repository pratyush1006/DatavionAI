"""Patient Billing architecture tests."""

from __future__ import annotations

from django.test import SimpleTestCase


class PatientBillingArchitectureTests(SimpleTestCase):
    """Protect critical Patient Billing architecture decisions."""

    def test_canonical_patient_reference(self) -> None:
        """Ensure Patient Billing uses the canonical Patient model."""

        from apps.billing.patient_billing.models import (
            PatientBillingAccount,
            PatientGuarantor,
        )

        self.assertEqual(
            PatientBillingAccount._meta.get_field(
                "patient",
            ).remote_field.model._meta.label,
            "patient_core.Patient",
        )
        self.assertEqual(
            PatientGuarantor._meta.get_field(
                "patient",
            ).remote_field.model._meta.label,
            "patient_core.Patient",
        )

    def test_canonical_patient_imports_are_used(self) -> None:
        """Ensure Patient Billing services use the canonical Patient model."""

        from apps.billing.patient_billing.services import guarantor as guarantor_service

        self.assertIs(
            guarantor_service.Patient,
            __import__(
                "apps.patient_management.patients.models",
                fromlist=["Patient"],
            ).Patient,
        )

    def test_workflow_exports_exist(self) -> None:
        """Ensure all mutation workflow boundaries are exported."""

        from apps.billing.patient_billing.workflows import (
            PatientBillingAccountWorkflow,
            PatientBillingStatementWorkflow,
            PatientGuarantorWorkflow,
            PatientResponsibilityWorkflow,
        )

        self.assertIsNotNone(PatientBillingAccountWorkflow)
        self.assertIsNotNone(PatientBillingStatementWorkflow)
        self.assertIsNotNone(PatientGuarantorWorkflow)
        self.assertIsNotNone(PatientResponsibilityWorkflow)


__all__ = ("PatientBillingArchitectureTests",)
