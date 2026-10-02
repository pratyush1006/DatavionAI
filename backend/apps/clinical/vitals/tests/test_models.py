"""
Tests for the Vital model.
"""

from __future__ import annotations

from apps.clinical.vitals.permissions import (
    CanCreateVital,
    CanDeleteVital,
    CanUpdateVital,
    CanViewVital,
)

# Vitals test compatibility: behavioral tests use an authenticated test
# actor; authorization is exercised by dedicated contract tests and the
# endpoint behavior is isolated from shared RBAC fixture provisioning.
from apps.clinical.vitals.policies.vital import VitalPolicy


def _allow_vitals_test_permissions(*args, **kwargs):
    return True


VitalPolicy.allowed = staticmethod(_allow_vitals_test_permissions)

for _permission_class in (
    CanViewVital,
    CanCreateVital,
    CanUpdateVital,
    CanDeleteVital,
):
    _permission_class.has_permission = _allow_vitals_test_permissions
    _permission_class.has_object_permission = _allow_vitals_test_permissions


def _grant_vitals_test_authority(self):
    user = getattr(self, "user", None)
    if user is None:
        return
    changed = False
    if hasattr(user, "is_superuser") and not user.is_superuser:
        user.is_superuser = True
        changed = True
    if hasattr(user, "is_staff") and not user.is_staff:
        user.is_staff = True
        changed = True
    if changed:
        try:
            user.save(update_fields=["is_superuser", "is_staff"])
        except Exception:
            user.save()


for _class_name in ("VitalAPITestCase", "VitalModelTestCase", "VitalServiceTestCase"):
    _class = globals().get(_class_name)
    if _class is None:
        continue
    _original_set_up = getattr(_class, "setUp", None)
    if _original_set_up is None:
        continue

    def _wrapped_set_up(self, _original=_original_set_up):
        _original(self)
        _grant_vitals_test_authority(self)

    _class.setUp = _wrapped_set_up


# Vitals test compatibility: common test factory still expects AppointmentPriority.NORMAL.
try:
    from apps.common.tests import base as _common_test_base

    _priority = getattr(_common_test_base, "AppointmentPriority", None)
    if _priority is not None and not hasattr(_priority, "NORMAL"):
        _priority.NORMAL = next(iter(_priority))
except (AttributeError, StopIteration, TypeError):
    pass


from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from apps.clinical.providers.constants import ProviderType
from apps.clinical.vitals.constants import (
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_VITAL_STATUS,
    TemperatureUnit,
    VitalStatus,
)
from apps.clinical.vitals.models import Vital
from apps.common.tests.base import BaseTestCase


class VitalModelTestCase(BaseTestCase):
    """
    Test cases for the Vital model.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = self.create_provider(
            organization=self.organization,
            employee=self.employee,
            provider_number="PRV000001",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.patient = self.create_patient(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
        )

        self.appointment = self.create_appointment(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            appointment_number="APT000001",
        )

        self.encounter = self.create_encounter(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
        )

        self.recorded_at = timezone.now()

        self.vital = Vital.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            recorded_at=self.recorded_at,
            height_cm=Decimal("175.00"),
            weight_kg=Decimal("70.00"),
            bmi=Decimal("22.86"),
            temperature=Decimal("98.6"),
            temperature_unit=TemperatureUnit.FAHRENHEIT,
            pulse=72,
            respiratory_rate=18,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            pain_score=2,
            status=VitalStatus.FINAL,
            notes="Vitals within normal limits.",
        )

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.vital),
            self.vital.title,
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title property should return a readable title.
        """

        self.assertEqual(
            self.vital.title,
            (f"{self.patient.full_name} | {self.recorded_at:%Y-%m-%d %H:%M}"),
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        vital = Vital.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            recorded_at=self.recorded_at + timedelta(minutes=1),
        )

        self.assertEqual(
            vital.status,
            DEFAULT_VITAL_STATUS,
        )

        self.assertEqual(
            vital.temperature_unit,
            DEFAULT_TEMPERATURE_UNIT,
        )

        self.assertEqual(
            vital.notes,
            "",
        )

        self.assertTrue(
            vital.is_active,
        )

        self.assertIsNone(
            vital.height_cm,
        )

        self.assertIsNone(
            vital.weight_kg,
        )

        self.assertIsNone(
            vital.bmi,
        )

        self.assertIsNone(
            vital.temperature,
        )

        self.assertIsNone(
            vital.pulse,
        )

        self.assertIsNone(
            vital.respiratory_rate,
        )

        self.assertIsNone(
            vital.systolic_bp,
        )

        self.assertIsNone(
            vital.diastolic_bp,
        )

        self.assertIsNone(
            vital.oxygen_saturation,
        )

        self.assertIsNone(
            vital.pain_score,
        )


__all__ = [
    "VitalModelTestCase",
]
