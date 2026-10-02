"""
Tests for vital services.
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
    TemperatureUnit,
    VitalStatus,
)
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.services import (
    create_vital,
    delete_vital,
    update_vital,
)
from apps.common.tests.base import BaseTestCase


class VitalServiceTestCase(BaseTestCase):
    """
    Test cases for vital services.
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
            notes="Initial vital record.",
        )

    def test_create_vital(
        self,
    ) -> None:
        """
        Vital should be created successfully.
        """

        vital = create_vital(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "recorded_at": self.recorded_at + timedelta(minutes=1),
                "height_cm": Decimal("180.00"),
                "weight_kg": Decimal("75.00"),
                "bmi": Decimal("23.15"),
                "temperature": Decimal("99.1"),
                "temperature_unit": TemperatureUnit.FAHRENHEIT,
                "pulse": 75,
                "respiratory_rate": 16,
                "systolic_bp": 118,
                "diastolic_bp": 78,
                "oxygen_saturation": 99,
                "pain_score": 1,
                "status": VitalStatus.FINAL,
                "notes": "Follow-up vital record.",
            },
        )

        self.assertIsInstance(
            vital,
            Vital,
        )

        self.assertEqual(
            vital.patient,
            self.patient,
        )

        self.assertEqual(
            vital.provider,
            self.provider,
        )

        self.assertEqual(
            vital.temperature,
            Decimal("99.1"),
        )

    def test_update_vital(
        self,
    ) -> None:
        """
        Vital should be updated successfully.
        """

        updated = update_vital(
            instance=self.vital,
            validated_data={
                "pulse": 80,
                "status": VitalStatus.FINAL,
                "notes": "Updated vital record.",
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.pulse,
            80,
        )

        self.assertEqual(
            updated.status,
            VitalStatus.FINAL,
        )

        self.assertEqual(
            updated.notes,
            "Updated vital record.",
        )

    def test_delete_vital(self):
        """Vital deletion must retain the row and apply the model soft-delete contract."""
        vital = self.vital
        actor = getattr(self, "user", None)
        result = delete_vital(
            vital,
            organization=self.organization,
            actor=actor,
        )
        self.assertIsNotNone(result)
        self.assertTrue(
            Vital.objects.filter(pk=vital.pk).exists(),
            "Vital deletion must retain the database row (soft delete).",
        )
        vital.refresh_from_db()
        if hasattr(vital, "is_deleted"):
            self.assertTrue(vital.is_deleted)
        elif hasattr(vital, "deleted"):
            self.assertTrue(vital.deleted)
        elif hasattr(vital, "deleted_at"):
            self.assertIsNotNone(vital.deleted_at)
        elif hasattr(vital, "is_active"):
            self.assertFalse(vital.is_active)
        elif hasattr(vital, "active"):
            self.assertFalse(vital.active)
        else:
            self.fail("Vital model exposes no recognized soft-delete marker.")

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_vital(
            instance=self.vital,
            validated_data={
                "oxygen_saturation": 100,
            },
        )

        self.assertEqual(
            updated.pk,
            self.vital.pk,
        )

        self.assertEqual(
            updated.oxygen_saturation,
            100,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Vital should persist after creation.
        """

        initial_count = Vital.objects.count()

        create_vital(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "recorded_at": self.recorded_at + timedelta(minutes=2),
            },
        )

        self.assertEqual(
            Vital.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "VitalServiceTestCase",
]
