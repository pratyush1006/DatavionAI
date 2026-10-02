from pathlib import Path

from django.test import SimpleTestCase


class ImagingArchitectureContractTests(SimpleTestCase):
    def test_canonical_module_is_apps_imaging(self):
        self.assertEqual(
            Path(__file__).resolve().parents[2].name,
            "imaging",
        )

    def test_protected_domains_are_not_imported_by_imaging(self):
        root = Path(__file__).resolve().parents[2]
        forbidden = (
            "apps.clinical",
            "apps.patient_management",
            "apps.patient_core",
            "apps.patient_family_members",
            "apps.billing.finance",
            "apps.platform.saas_billing",
        )
        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                self.assertNotIn(
                    value,
                    text,
                    msg=f"Protected-domain import detected in {path}: {value}",
                )

    def test_integration_boundaries_exist(self):
        root = Path(__file__).resolve().parents[2]
        for relative in (
            "integrations/appointments",
            "integrations/documents",
            "integrations/revenue_cycle",
            "integrations/storage",
            "integrations/pacs",
        ):
            self.assertTrue((root / relative).is_dir(), relative)
