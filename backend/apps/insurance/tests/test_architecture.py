from django.test import SimpleTestCase

from apps.core.models import BaseModel
from apps.insurance.models import (
    TPA,
    Benefit,
    CoordinationOfBenefits,
    Dependent,
    Enrollment,
    InsurancePlan,
    MemberIdentifier,
    Network,
    Payer,
    PayerTPARelationship,
    PlanProduct,
    Subscriber,
)


class InsuranceArchitectureTests(SimpleTestCase):
    """Verify the canonical Insurance bounded-context contract."""

    models = (
        Payer,
        TPA,
        PayerTPARelationship,
        InsurancePlan,
        PlanProduct,
        Network,
        Subscriber,
        Enrollment,
        Dependent,
        MemberIdentifier,
        Benefit,
        CoordinationOfBenefits,
    )

    def test_insurance_models_use_base_model(self):
        for model in self.models:
            with self.subTest(model=model.__name__):
                self.assertTrue(issubclass(model, BaseModel))

    def test_tpa_is_first_class(self):
        self.assertIsNotNone(PayerTPARelationship._meta.get_field("payer"))
        self.assertIsNotNone(PayerTPARelationship._meta.get_field("tpa"))
        self.assertIsNotNone(PayerTPARelationship._meta.get_field("effective_date"))
        self.assertIsNotNone(PayerTPARelationship._meta.get_field("termination_date"))

    def test_canonical_patient(self):
        field = Enrollment._meta.get_field("patient")
        self.assertEqual(
            field.remote_field.model._meta.label_lower, "patient_core.patient"
        )

    def test_operational_duplicates_are_not_exported(self):
        import apps.insurance.models as module

        self.assertFalse(hasattr(module, "Claim"))
        self.assertFalse(hasattr(module, "Authorization"))

    def test_revenue_cycle_owns_operational_flow(self):
        import apps.insurance.models as module

        exported = set(module.__all__)
        self.assertNotIn("Claim", exported)
        self.assertNotIn("Authorization", exported)
