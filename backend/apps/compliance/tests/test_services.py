"""
Smoke tests for the Compliance (HIPAA) services.
"""

from __future__ import annotations

from apps.clinical.patients.tests.factories import PatientFactory
from apps.common.tests.base import BaseTestCase
from apps.compliance.constants import (
    ConsentPurpose,
    ConsentStatus,
    PhiAccessAction,
)
from apps.compliance.models import Consent, PhiAccessLog
from apps.compliance.services import (
    FieldEncryption,
    PhiAccessLogger,
)


class ComplianceServiceTestCase(BaseTestCase):
    """
    Verify consent, PHI audit logging and field encryption.
    """

    def test_phi_access_logger(self) -> None:
        patient = PatientFactory(organization=self.organization)

        log = PhiAccessLogger.log(
            action=PhiAccessAction.VIEW,
            actor=self.admin,
            patient=patient,
            organization=self.organization,
            resource_type="ClinicalNote",
            resource_id="abc",
        )

        self.assertIsInstance(log, PhiAccessLog)
        self.assertEqual(log.action, PhiAccessAction.VIEW)
        self.assertEqual(PhiAccessLog.objects.count(), 1)

    def test_consent_lifecycle(self) -> None:
        patient = PatientFactory(organization=self.organization)

        consent = Consent.objects.create(
            patient=patient,
            organization=self.organization,
            purpose=ConsentPurpose.TREATMENT,
            status=ConsentStatus.GRANTED,
        )

        self.assertEqual(consent.status, ConsentStatus.GRANTED)

    def test_field_encryption_round_trip(self) -> None:
        cipher = FieldEncryption()
        token = cipher.encrypt("secret-value")

        self.assertNotEqual(token, "secret-value")
        self.assertEqual(cipher.decrypt(token), "secret-value")

    def test_field_encryption_rejects_unknown_action(self) -> None:
        with self.assertRaises(ValueError):
            PhiAccessLogger.log(
                action="not-a-real-action",
                actor=self.admin,
            )
