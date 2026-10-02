from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]


class ImagingDomainBoundaryTests(SimpleTestCase):
    def test_domain_model_boundaries_exist(self):
        required = (
            "modality.py",
            "order.py",
            "procedure.py",
            "study.py",
            "contrast.py",
            "finding.py",
            "report.py",
            "appointments.py",
            "documents.py",
            "revenue_cycle.py",
            "audit.py",
        )
        for name in required:
            self.assertTrue((ROOT / "models" / name).exists(), name)

    def test_domain_service_boundaries_exist(self):
        required = (
            "orders.py",
            "scheduling.py",
            "worklist.py",
            "procedures.py",
            "acquisition.py",
            "contrast.py",
            "findings.py",
            "reporting.py",
            "appointments.py",
            "documents.py",
            "revenue_cycle.py",
            "storage.py",
            "pacs.py",
        )
        for name in required:
            self.assertTrue((ROOT / "services" / name).exists(), name)

    def test_integration_contracts_are_explicit(self):
        for rel in (
            "appointments/contracts.py",
            "documents/contracts.py",
            "revenue_cycle/contracts.py",
            "storage/contracts.py",
            "pacs/contracts.py",
        ):
            self.assertTrue((ROOT / "integrations" / rel).exists(), rel)
