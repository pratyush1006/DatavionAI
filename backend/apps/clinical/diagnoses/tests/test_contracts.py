from django.test import SimpleTestCase

from apps.clinical.diagnoses.constants import DiagnosisStatus, DiagnosisType


class DiagnosisContractTests(SimpleTestCase):
    def test_status_contract(self):
        self.assertEqual(
            set(DiagnosisStatus.values),
            {"active", "resolved", "inactive", "ruled_out"},
        )

    def test_type_contract(self):
        self.assertEqual(
            set(DiagnosisType.values),
            {"primary", "secondary", "differential", "historical"},
        )
