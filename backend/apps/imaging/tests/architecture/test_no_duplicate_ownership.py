from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[3]


class ImagingOwnershipBoundaryTests(SimpleTestCase):
    def test_protected_domains_are_not_reimplemented(self):
        imaging = ROOT / "apps" / "imaging"
        for path in imaging.rglob("*.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("class HealthcareInvoice", text)
            self.assertNotIn("class Patient(", text)
            self.assertNotIn("class Appointment(", text)
            self.assertNotIn("class Document(", text)
