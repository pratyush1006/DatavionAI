from __future__ import annotations

import importlib
from pathlib import Path

from django.test import SimpleTestCase


class InsuranceRevenueCycleE2EContractTests(SimpleTestCase):
    """Executable contract for the canonical Insurance -> RCM boundary."""

    def test_insurance_exports_canonical_master_data(self) -> None:
        module = importlib.import_module("apps.insurance.models")
        exported = set(getattr(module, "__all__", ()))
        required = {
            "Payer",
            "TPA",
            "PayerTPARelationship",
            "InsurancePlan",
            "PlanProduct",
            "Network",
            "Subscriber",
            "Enrollment",
            "Dependent",
            "MemberIdentifier",
            "Benefit",
            "CoordinationOfBenefits",
        }
        missing = sorted(required - exported)
        self.assertFalse(missing, f"Insurance exports are incomplete: {missing}")
        self.assertFalse(hasattr(module, "Claim"))
        self.assertFalse(hasattr(module, "Authorization"))

    def test_insurance_enrollment_uses_canonical_patient(self) -> None:
        enrollment = importlib.import_module("apps.insurance.models").Enrollment
        field = enrollment._meta.get_field("patient")
        self.assertEqual(
            field.remote_field.model._meta.label_lower,
            "patient_core.patient",
        )

    def test_payer_tpa_relationship_is_first_class(self) -> None:
        relationship = importlib.import_module(
            "apps.insurance.models"
        ).PayerTPARelationship
        for name in ("payer", "tpa", "effective_date", "termination_date"):
            self.assertIsNotNone(relationship._meta.get_field(name))

    def test_insurance_route_resolution_contract(self) -> None:
        services = importlib.import_module("apps.insurance.services")
        resolver = getattr(services, "resolve_route", None)
        self.assertTrue(callable(resolver))

        source = Path(services.__file__).read_text(
            encoding="utf-8",
            errors="ignore",
        )
        self.assertIn("payer.tpa_relationships", source)

    def test_integration_record_contract(self) -> None:
        model = importlib.import_module(
            "apps.revenue_cycle.cross_module_integration.models"
        ).RevenueCycleIntegrationRecord
        self.assertEqual(
            model._meta.db_table,
            "revenue_cycle_integration_records",
        )
        fields = {
            field.name
            for field in model._meta.get_fields()
            if getattr(field, "concrete", False)
        }
        required = {"organization", "source", "event_type", "payload"}
        missing = sorted(required - fields)
        self.assertFalse(missing, f"Missing integration fields: {missing}")

    def test_integration_sources_cover_operational_chain(self) -> None:
        constants = importlib.import_module(
            "apps.revenue_cycle.cross_module_integration.constants"
        )
        required = {
            "ELIGIBILITY",
            "INSURANCE_VERIFICATION",
            "PRIOR_AUTHORIZATION",
            "CHARGE_CAPTURE",
            "CODING",
            "CLAIM_SCRUBBING",
            "CLAIM_SUBMISSION",
            "PAYMENT_POSTING",
            "ERA",
            "DENIALS",
            "APPEALS",
            "ACCOUNTS_RECEIVABLE",
            "REVENUE_ANALYTICS",
        }
        available = {item.name for item in constants.IntegrationSource}
        missing = sorted(required - available)
        self.assertFalse(missing, f"Missing integration sources: {missing}")

    def test_revenue_cycle_operational_models_exist(self) -> None:
        required = {
            "apps.revenue_cycle.insurance_verification.models": "InsuranceVerification",
            "apps.revenue_cycle.eligibility.models.eligibility": "Eligibility",
            "apps.revenue_cycle.prior_authorization.models.prior_authorization": "PriorAuthorization",
            "apps.revenue_cycle.charge_capture.models.charge": "Charge",
            "apps.revenue_cycle.coding.models.coding_record": "CodingRecord",
            "apps.revenue_cycle.claim_scrubbing.models.claim_scrub": "ClaimScrub",
            "apps.revenue_cycle.claim_submission.models.claim_submission": "ClaimSubmission",
            "apps.revenue_cycle.era.models.era": "ERA",
            "apps.revenue_cycle.payment_posting.models.payment_posting": "PaymentPosting",
            "apps.revenue_cycle.denials.models.denial": "Denial",
            "apps.revenue_cycle.appeals.models.appeal": "Appeal",
            "apps.revenue_cycle.accounts_receivable.models": "ARAccount",
            "apps.revenue_cycle.revenue_analytics.models": "RevenueMetricSnapshot",
        }
        missing = []
        for module_path, class_name in required.items():
            module = importlib.import_module(module_path)
            if not hasattr(module, class_name):
                missing.append(f"{module_path}.{class_name}")
        self.assertFalse(missing, f"Missing RCM operational models: {missing}")

    def test_root_urls_keep_both_bounded_contexts(self) -> None:
        backend_root = Path(__file__).resolve().parents[5]
        root_text = None
        for path in backend_root.rglob("urls.py"):
            if "venv" in path.parts or "backups" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "apps.revenue_cycle.urls" in text:
                root_text = text
                break
        self.assertIsNotNone(root_text)
        self.assertIn("apps.insurance.urls", root_text)
        self.assertIn("apps.revenue_cycle.urls", root_text)

    def test_no_retired_or_duplicate_ownership_dependency(self) -> None:
        backend_root = Path(__file__).resolve().parents[5]
        roots = (
            backend_root / "apps" / "insurance",
            backend_root / "apps" / "revenue_cycle",
        )
        forbidden = (
            "apps.clinical.patients",
            "apps.insurance.models.claim",
            "apps.insurance.models.authorization",
        )
        hits = []
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*.py"):
                text = path.read_text(encoding="utf-8", errors="ignore")
                for token in forbidden:
                    if token in text:
                        hits.append(f"{path.relative_to(backend_root)} -> {token}")
        self.assertFalse(
            hits,
            "Forbidden ownership/dependency references: " + str(hits),
        )
