from __future__ import annotations

import importlib
import inspect
import json
from pathlib import Path

from django.test import SimpleTestCase


class InsuranceRevenueCycleRuntimeContractTests(SimpleTestCase):
    """Validate the current LIVE Insurance -> RCM runtime surface."""

    SERVICE_MODULES = (
        (
            "insurance_verification",
            "apps.revenue_cycle.insurance_verification.services",
        ),
        ("eligibility", "apps.revenue_cycle.eligibility.services"),
        ("prior_authorization", "apps.revenue_cycle.prior_authorization.services"),
        ("charge_capture", "apps.revenue_cycle.charge_capture.services"),
        ("coding", "apps.revenue_cycle.coding.services"),
        ("claim_scrubbing", "apps.revenue_cycle.claim_scrubbing.services"),
        ("claim_submission", "apps.revenue_cycle.claim_submission.services"),
        ("era", "apps.revenue_cycle.era.services"),
        ("payment_posting", "apps.revenue_cycle.payment_posting.services"),
        ("denials", "apps.revenue_cycle.denials.services"),
        ("appeals", "apps.revenue_cycle.appeals.services"),
        ("accounts_receivable", "apps.revenue_cycle.accounts_receivable.services"),
        ("revenue_analytics", "apps.revenue_cycle.revenue_analytics.services"),
    )

    MODEL_CONTRACTS = (
        ("apps.revenue_cycle.insurance_verification.models", "InsuranceVerification"),
        ("apps.revenue_cycle.eligibility.models", "Eligibility"),
        ("apps.revenue_cycle.prior_authorization.models", "PriorAuthorization"),
        ("apps.revenue_cycle.charge_capture.models", "Charge"),
        ("apps.revenue_cycle.coding.models", "CodingRecord"),
        ("apps.revenue_cycle.claim_scrubbing.models", "ClaimScrub"),
        ("apps.revenue_cycle.claim_submission.models", "ClaimSubmission"),
        ("apps.revenue_cycle.era.models", "ERA"),
        ("apps.revenue_cycle.payment_posting.models", "PaymentPosting"),
        ("apps.revenue_cycle.denials.models", "Denial"),
        ("apps.revenue_cycle.appeals.models", "Appeal"),
        ("apps.revenue_cycle.accounts_receivable.models", "ARAccount"),
        ("apps.revenue_cycle.revenue_analytics.models", "RevenueMetricSnapshot"),
        (
            "apps.revenue_cycle.cross_module_integration.models",
            "RevenueCycleIntegrationRecord",
        ),
    )

    EXPECTED_FUNCTIONS = {
        "claim_submission": {
            "create_submission",
            "update_submission",
            "delete_submission",
        },
        "payment_posting": {
            "create_payment_posting",
            "post_payment",
            "delete_payment_posting",
            "restore_payment_posting",
        },
        "denials": {
            "create_denial",
            "transition_denial",
            "delete_denial",
        },
    }

    def test_all_live_service_modules_import(self) -> None:
        failures: list[str] = []

        for context, module_path in self.SERVICE_MODULES:
            try:
                importlib.import_module(module_path)
            except Exception as exc:
                failures.append(
                    f"{context}: {module_path}: {type(exc).__name__}: {exc}"
                )

        self.assertFalse(
            failures,
            "Live service module failures: " + "; ".join(failures),
        )

    def test_live_service_callable_surface_is_present(self) -> None:
        failures: list[str] = []

        for context, module_path in self.SERVICE_MODULES:
            module = importlib.import_module(module_path)

            public_callables = [
                name
                for name in dir(module)
                if not name.startswith("_") and callable(getattr(module, name, None))
            ]

            if not public_callables:
                failures.append(
                    f"{context}: no public callable service surface in {module_path}"
                )

        self.assertFalse(
            failures,
            "Service callable-surface failures: " + "; ".join(failures),
        )

    def test_required_live_operations_are_reachable(self) -> None:
        failures: list[str] = []

        for context, required_names in self.EXPECTED_FUNCTIONS.items():
            module_path = dict(self.SERVICE_MODULES)[context]
            module = importlib.import_module(module_path)

            for name in sorted(required_names):
                if not callable(getattr(module, name, None)):
                    failures.append(
                        f"{context}: missing operation {module_path}.{name}"
                    )

        self.assertFalse(
            failures,
            "Required live service operations missing: " + "; ".join(failures),
        )

    def test_live_service_signatures_are_extractable(self) -> None:
        failures: list[str] = []
        inspected = 0

        for context, module_path in self.SERVICE_MODULES:
            module = importlib.import_module(module_path)

            for name in dir(module):
                if name.startswith("_"):
                    continue

                attribute = getattr(module, name, None)
                if not callable(attribute):
                    continue

                # Only inspect application-level callables defined by the
                # service module; imported framework/helper callables are not
                # part of this runtime contract.
                if getattr(attribute, "__module__", None) != module.__name__:
                    continue

                try:
                    inspect.signature(attribute)
                except (TypeError, ValueError) as exc:
                    failures.append(
                        f"{context}: {module_path}.{name}: signature unavailable: {exc}"
                    )
                    continue

                inspected += 1

        self.assertGreater(
            inspected,
            0,
            "No live service callables were introspected.",
        )
        self.assertFalse(
            failures,
            "Service signature failures: " + "; ".join(failures),
        )

    def test_live_models_are_importable(self) -> None:
        failures: list[str] = []

        for module_path, class_name in self.MODEL_CONTRACTS:
            try:
                module = importlib.import_module(module_path)
            except Exception as exc:
                failures.append(f"{module_path}: {type(exc).__name__}: {exc}")
                continue

            if not hasattr(module, class_name):
                failures.append(f"{module_path}.{class_name}")

        self.assertFalse(
            failures,
            "Missing live RCM models: " + "; ".join(failures),
        )

    def test_model_labels_are_unique(self) -> None:
        labels: list[str] = []

        for module_path, class_name in self.MODEL_CONTRACTS:
            model = getattr(
                importlib.import_module(module_path),
                class_name,
            )
            labels.append(model._meta.label_lower)

        self.assertEqual(
            len(labels),
            len(set(labels)),
            "RCM model labels collide: " + ", ".join(labels),
        )

    def test_insurance_boundary_remains_canonical(self) -> None:
        module = importlib.import_module("apps.insurance.models")

        self.assertFalse(hasattr(module, "Claim"))
        self.assertFalse(hasattr(module, "Authorization"))

        enrollment = module.Enrollment
        patient_model = enrollment._meta.get_field("patient").remote_field.model

        self.assertEqual(
            patient_model._meta.label_lower,
            "patient_core.patient",
        )

        services = importlib.import_module("apps.insurance.services")
        self.assertTrue(callable(getattr(services, "resolve_route", None)))

    def test_integration_boundary_remains_wired(self) -> None:
        model = importlib.import_module(
            "apps.revenue_cycle.cross_module_integration.models"
        ).RevenueCycleIntegrationRecord

        fields = {
            field.name
            for field in model._meta.get_fields()
            if getattr(field, "concrete", False)
        }

        self.assertTrue(
            {"organization", "source", "event_type", "payload"}.issubset(fields)
        )

    def test_manifest_declares_no_schema_change(self) -> None:
        backend_root = Path(__file__).resolve().parents[4]
        manifest = (
            backend_root
            / "apps"
            / "revenue_cycle"
            / "cross_module_integration"
            / "insurance_revenue_cycle_runtime_contract.json"
        )

        self.assertTrue(
            manifest.exists(),
            f"Missing runtime manifest: {manifest}",
        )

        payload = json.loads(manifest.read_text(encoding="utf-8"))

        self.assertFalse(payload["schema_changes"])
        self.assertFalse(payload["database_rows_created"])
        self.assertEqual(payload["version"], "1.1.6")
