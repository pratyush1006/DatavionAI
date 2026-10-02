from __future__ import annotations

import importlib
import inspect
import json
from pathlib import Path
from pkgutil import walk_packages
from typing import Any

from django.db import connection, transaction
from django.test import TransactionTestCase


class InsuranceRevenueCycleTransactionalE2ETests(TransactionTestCase):
    """Insurance -> Revenue Cycle transactional readiness contract."""

    reset_sequences = True

    SERVICE_MODULES = {
        "insurance_verification": "apps.revenue_cycle.insurance_verification.services",
        "eligibility": "apps.revenue_cycle.eligibility.services",
        "prior_authorization": "apps.revenue_cycle.prior_authorization.services",
        "charge_capture": "apps.revenue_cycle.charge_capture.services",
        "coding": "apps.revenue_cycle.coding.services",
        "claim_scrubbing": "apps.revenue_cycle.claim_scrubbing.services",
        "claim_submission": "apps.revenue_cycle.claim_submission.services",
        "era": "apps.revenue_cycle.era.services",
        "payment_posting": "apps.revenue_cycle.payment_posting.services",
        "denials": "apps.revenue_cycle.denials.services",
        "appeals": "apps.revenue_cycle.appeals.services",
        "accounts_receivable": "apps.revenue_cycle.accounts_receivable.services",
        "revenue_analytics": "apps.revenue_cycle.revenue_analytics.services",
    }

    WORKFLOW_MODULES = {
        "insurance_verification": "apps.revenue_cycle.insurance_verification.workflows",
        "eligibility": "apps.revenue_cycle.eligibility.workflows",
        "prior_authorization": "apps.revenue_cycle.prior_authorization.workflows",
        "charge_capture": "apps.revenue_cycle.charge_capture.workflows",
        "coding": "apps.revenue_cycle.coding.workflows",
        "claim_scrubbing": "apps.revenue_cycle.claim_scrubbing.workflows",
        "claim_submission": "apps.revenue_cycle.claim_submission.workflows",
        "era": "apps.revenue_cycle.era.workflows",
        "payment_posting": "apps.revenue_cycle.payment_posting.workflows",
        "denials": "apps.revenue_cycle.denials.workflows",
        "appeals": "apps.revenue_cycle.appeals.workflows",
        "accounts_receivable": "apps.revenue_cycle.accounts_receivable.workflows",
        "revenue_analytics": "apps.revenue_cycle.revenue_analytics.workflows",
    }

    MODEL_CONTRACTS = (
        ("apps.insurance.models", "Payer"),
        ("apps.insurance.models", "TPA"),
        ("apps.insurance.models", "PayerTPARelationship"),
        ("apps.insurance.models", "InsurancePlan"),
        ("apps.insurance.models", "Enrollment"),
        ("apps.insurance.models", "Benefit"),
        ("apps.insurance.models", "CoordinationOfBenefits"),
        (
            "apps.revenue_cycle.cross_module_integration.models",
            "RevenueCycleIntegrationRecord",
        ),
    )

    TRANSACTIONAL_SERVICE_CONTEXTS = (
        "charge_capture",
        "claim_submission",
        "claim_scrubbing",
        "payment_posting",
        "denials",
        "era",
        "appeals",
        "accounts_receivable",
        "revenue_analytics",
    )

    MIGRATION = Path("apps/revenue_cycle/migrations/0001_initial.py")
    MANIFEST = Path(
        "apps/revenue_cycle/cross_module_integration/"
        "insurance_revenue_cycle_transactional_e2e.json"
    )

    @classmethod
    def _module_tree(cls, module: Any) -> list[Any]:
        modules = [module]
        package_path = getattr(module, "__path__", None)
        if package_path is None:
            return modules

        seen = {module.__name__}
        for info in walk_packages(package_path, module.__name__ + "."):
            try:
                child = importlib.import_module(info.name)
            except Exception:
                continue
            if child.__name__ not in seen:
                seen.add(child.__name__)
                modules.append(child)
        return modules

    @classmethod
    def _service_surface(cls, module_path: str) -> bool:
        try:
            root = importlib.import_module(module_path)
        except Exception:
            return False

        for module in cls._module_tree(root):
            for name, value in vars(module).items():
                if name.startswith("_"):
                    continue

                if inspect.isfunction(value):
                    return True

                if inspect.isclass(value):
                    for method_name in dir(value):
                        if method_name.startswith("_"):
                            continue
                        try:
                            method = getattr(value, method_name)
                        except Exception:
                            continue
                        if callable(method):
                            return True
        return False

    @classmethod
    def _workflow_surface(cls, module_path: str) -> bool:
        """
        Accept both execute()-style workflows and domain-operation workflow
        classes used by the live Revenue Cycle architecture.
        """
        try:
            root = importlib.import_module(module_path)
        except Exception:
            return False

        ignored = {
            "save",
            "delete",
            "full_clean",
            "clean",
            "validate",
            "refresh_from_db",
        }

        for module in cls._module_tree(root):
            for name, candidate in vars(module).items():
                if name.startswith("_") or not inspect.isclass(candidate):
                    continue

                if getattr(candidate, "__module__", None) != module.__name__:
                    continue

                for method_name, method in inspect.getmembers(candidate):
                    if method_name.startswith("_") or method_name in ignored:
                        continue
                    if callable(method):
                        return True
        return False

    @staticmethod
    def _sources(module_path: str) -> str:
        try:
            root = importlib.import_module(module_path)
        except Exception:
            return ""

        paths = []
        root_file = getattr(root, "__file__", None)
        if root_file:
            paths.append(Path(root_file))

        package_path = getattr(root, "__path__", None)
        if package_path is not None:
            for module in InsuranceRevenueCycleTransactionalE2ETests._module_tree(root):
                source_file = getattr(module, "__file__", None)
                if source_file:
                    paths.append(Path(source_file))

        output = []
        seen = set()

        for path in paths:
            try:
                resolved = path.resolve()
            except Exception:
                resolved = path

            if resolved in seen:
                continue
            seen.add(resolved)

            try:
                output.append(
                    path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )
            except Exception:
                continue

        return "\n".join(output)

    def test_models_import(self):
        failures = []
        for module_path, model_name in self.MODEL_CONTRACTS:
            try:
                getattr(importlib.import_module(module_path), model_name)
            except Exception as exc:
                failures.append(f"{module_path}.{model_name}: {exc}")
        self.assertFalse(failures, "; ".join(failures))

    def test_enrollment_uses_canonical_patient(self):
        enrollment = importlib.import_module("apps.insurance.models").Enrollment

        field = enrollment._meta.get_field("patient")

        self.assertEqual(
            field.remote_field.model._meta.label_lower,
            "patient_core.patient",
        )

    def test_service_modules_import(self):
        failures = []

        for context, module_path in self.SERVICE_MODULES.items():
            try:
                importlib.import_module(module_path)
            except Exception as exc:
                failures.append(f"{context}: {exc}")

        self.assertFalse(
            failures,
            "; ".join(failures),
        )

    def test_service_surfaces_exist(self):
        failures = [
            context
            for context, module_path in self.SERVICE_MODULES.items()
            if not self._service_surface(module_path)
        ]

        self.assertFalse(
            failures,
            "Missing service surfaces: " + ", ".join(failures),
        )

    def test_workflow_modules_import(self):
        failures = []

        for context, module_path in self.WORKFLOW_MODULES.items():
            try:
                importlib.import_module(module_path)
            except Exception as exc:
                failures.append(f"{context}: {exc}")

        self.assertFalse(
            failures,
            "; ".join(failures),
        )

    def test_workflow_surfaces_exist(self):
        failures = [
            context
            for context, module_path in self.WORKFLOW_MODULES.items()
            if not self._workflow_surface(module_path)
        ]

        self.assertFalse(
            failures,
            "Missing workflow surfaces: " + ", ".join(failures),
        )

    def test_transaction_commit_on_commit_callback(self):
        state = {"called": False}

        with transaction.atomic():
            self.assertTrue(connection.in_atomic_block)

            transaction.on_commit(lambda: state.__setitem__("called", True))

            self.assertFalse(state["called"])

        self.assertFalse(connection.in_atomic_block)
        self.assertTrue(state["called"])

    def test_transaction_rollback_discards_callback(self):
        state = {"called": False}

        try:
            with transaction.atomic():
                transaction.on_commit(lambda: state.__setitem__("called", True))

                raise RuntimeError("intentional rollback")
        except RuntimeError:
            pass

        self.assertFalse(connection.in_atomic_block)
        self.assertFalse(state["called"])

    def test_selected_services_have_transaction_boundary(self):
        failures = []

        for context in self.TRANSACTIONAL_SERVICE_CONTEXTS:
            source = self._sources(self.SERVICE_MODULES[context])

            if not any(
                marker in source
                for marker in (
                    "@transaction.atomic",
                    "transaction.atomic(",
                )
            ):
                failures.append(context)

        self.assertFalse(
            failures,
            "Missing transaction.atomic boundary: " + ", ".join(failures),
        )

    def test_migration_baseline(self):
        self.assertTrue(
            self.MIGRATION.is_file(),
            str(self.MIGRATION),
        )

        source = self.MIGRATION.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        self.assertNotIn(
            "patients.patient",
            source,
        )
        self.assertNotIn(
            "('patients', '0001_initial')",
            source,
        )
        self.assertIn(
            "patient_core.patient",
            source,
        )
        self.assertIn(
            "organizations.organization",
            source,
        )

    def test_manifest(self):
        self.assertTrue(
            self.MANIFEST.is_file(),
            str(self.MANIFEST),
        )

        raw = self.MANIFEST.read_text(
            encoding="utf-8",
            errors="strict",
        )

        manifest = json.loads(raw)

        self.assertIsInstance(manifest, dict)

        self.assertEqual(
            manifest.get("harness_version"),
            "1.0.8",
        )
        self.assertEqual(
            manifest.get("business_e2e_status"),
            "PENDING_LIVE_PAYLOAD_BINDING",
        )
        self.assertEqual(
            manifest.get("production_database_writes"),
            "NONE",
        )
        self.assertEqual(
            manifest.get("schema_changes"),
            "NONE",
        )

        verified = manifest.get(
            "verified_flow",
            [],
        )

        self.assertIn(
            "transaction.on_commit success semantics",
            verified,
        )
        self.assertIn(
            "transaction rollback semantics",
            verified,
        )

        self.assertTrue(
            manifest.get("blocked_from_full_business_e2e"),
        )
