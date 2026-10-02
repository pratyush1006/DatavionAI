from __future__ import annotations

import uuid
from datetime import timedelta
from decimal import Decimal

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from apps.hospital_operations.constants import BedStatus, ReservationStatus
from apps.hospital_operations.models import (
    Admission,
    Bed,
    BedAssignment,
    BedReservation,
    Facility,
    OPDQueue,
    OPDVisit,
    OperationalUnit,
    Room,
)
from apps.hospital_operations.services import (
    assign_bed,
    complete_room_cleaning,
    discharge_patient,
    register_opd_visit,
    release_bed,
    reserve_bed,
    transfer_patient,
)


def _create_root(model_label, context=None):
    model = apps.get_model(*model_label.split("."))
    context = dict(context or {})
    values = {}
    suffix = uuid.uuid4().hex[:10]
    for field in model._meta.fields:
        if (
            field.primary_key
            or field.auto_created
            or getattr(field, "auto_now", False)
            or getattr(field, "auto_now_add", False)
        ):
            continue
        if field.name in context:
            values[field.name] = context[field.name]
            continue
        if field.has_default() or field.null:
            continue
        if field.is_relation:
            related = field.remote_field.model
            label = related._meta.label_lower
            if label == "tenancy.tenant":
                values[field.name] = _create_root("tenancy.Tenant")
            elif label == "organizations.organization":
                tenant = context.get("tenant") or _create_root("tenancy.Tenant")
                values[field.name] = _create_root(
                    "organizations.Organization", {"tenant": tenant}
                )
            elif label == "patient_core.patient":
                tenant = context.get("tenant") or _create_root("tenancy.Tenant")
                organization = context.get("organization") or _create_root(
                    "organizations.Organization", {"tenant": tenant}
                )
                values[field.name] = _create_root(
                    "patient_core.Patient",
                    {"tenant": tenant, "organization": organization},
                )
            else:
                raise RuntimeError(
                    f"Unsupported required fixture relation: {model._meta.label}.{field.name} -> {label}"
                )
            continue
        internal = field.get_internal_type()
        name = field.name.lower()
        if internal in {"CharField", "TextField", "SlugField"}:
            if "email" in name:
                candidate = f"e2e-{suffix}@example.test"
            elif "phone" in name:
                candidate = f"90000{suffix[:5]}"
            elif any(token in name for token in ("code", "number", "mrn", "slug")):
                candidate = f"E2E-{suffix}"
            elif "name" in name:
                candidate = f"Hospital Operations E2E {suffix}"
            else:
                candidate = "Hospital Operations E2E"
            max_length = getattr(field, "max_length", None)
            if max_length is not None:
                candidate = candidate[:max_length]
            values[field.name] = candidate
        elif internal == "DateField":
            values[field.name] = timezone.localdate()
        elif internal == "DateTimeField":
            values[field.name] = timezone.now()
        elif internal == "BooleanField":
            values[field.name] = False
        elif internal in {
            "IntegerField",
            "PositiveIntegerField",
            "PositiveSmallIntegerField",
            "SmallIntegerField",
        }:
            values[field.name] = 1
        elif internal in {"DecimalField", "FloatField"}:
            values[field.name] = Decimal("1")
        elif internal == "JSONField":
            values[field.name] = {}
        elif internal == "UUIDField":
            values[field.name] = uuid.uuid4()
        else:
            raise RuntimeError(
                f"Unsupported required fixture field: {model._meta.label}.{field.name}"
            )
    return model.objects.create(**values)


class HospitalOperationsRuntimeExecutionTests(TestCase):
    def setUp(self):
        self.tenant = _create_root("tenancy.Tenant")
        self.organization = _create_root(
            "organizations.Organization", {"tenant": self.tenant}
        )
        self.patient = _create_root(
            "patient_core.Patient",
            {"tenant": self.tenant, "organization": self.organization},
        )
        self.facility = Facility.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            name="E2E Facility",
            code=f"FAC-{uuid.uuid4().hex[:8]}",
        )
        self.unit = OperationalUnit.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            facility=self.facility,
            name="E2E Ward",
            code=f"WARD-{uuid.uuid4().hex[:8]}",
            unit_type="ward",
        )
        self.icu_unit = OperationalUnit.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            facility=self.facility,
            name="E2E ICU",
            code=f"ICU-{uuid.uuid4().hex[:8]}",
            unit_type="icu",
        )
        self.room = Room.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            facility=self.facility,
            unit=self.unit,
            number=f"R-{uuid.uuid4().hex[:6]}",
            capacity=1,
        )
        self.icu_room = Room.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            facility=self.facility,
            unit=self.icu_unit,
            number=f"ICU-R-{uuid.uuid4().hex[:6]}",
            capacity=1,
        )
        self.bed = Bed.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            room=self.room,
            label="B1",
        )
        self.icu_bed = Bed.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            room=self.icu_room,
            label="ICU-B1",
        )
        self.opd_queue = OPDQueue.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            unit=self.unit,
            name="E2E OPD",
            queue_date=timezone.localdate(),
        )

    def test_opd_registration_is_transactional_and_sequential(self):
        first = register_opd_visit(
            queue=self.opd_queue,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
        )
        second = register_opd_visit(
            queue=self.opd_queue,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
        )
        self.assertEqual((first.token_number, second.token_number), (1, 2))
        self.opd_queue.refresh_from_db()
        self.assertEqual(self.opd_queue.current_token, 2)
        self.assertEqual(OPDVisit.objects.filter(queue=self.opd_queue).count(), 2)

    def test_reservation_assignment_release_cleaning_lifecycle(self):
        reservation = reserve_bed(
            bed=self.bed,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
            reserved_from=timezone.now(),
            reserved_until=timezone.now() + timedelta(hours=4),
            reference="E2E",
        )
        self.bed.refresh_from_db()
        self.assertEqual(reservation.status, ReservationStatus.ACTIVE.value)
        self.assertEqual(self.bed.status, BedStatus.RESERVED.value)
        assignment = assign_bed(
            bed=self.bed,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
            admission_reference="E2E-ADM",
            reservation=reservation,
        )
        self.bed.refresh_from_db()
        reservation.refresh_from_db()
        self.assertEqual(self.bed.status, BedStatus.OCCUPIED.value)
        self.assertEqual(reservation.status, ReservationStatus.FULFILLED.value)
        self.assertTrue(assignment.active)
        release_bed(
            assignment=assignment, tenant=self.tenant, organization=self.organization
        )
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, BedStatus.CLEANING.value)
        complete_room_cleaning(
            bed=self.bed, tenant=self.tenant, organization=self.organization
        )
        self.bed.refresh_from_db()
        self.assertEqual(self.bed.status, BedStatus.AVAILABLE.value)

    def test_admission_transfer_icu_discharge_lifecycle(self):
        admission = Admission.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            patient=self.patient,
            unit=self.unit,
            admission_number=f"ADM-{uuid.uuid4().hex[:10]}",
            admitted_at=timezone.now(),
            reason="E2E",
        )
        admission.bed_assignment = assign_bed(
            bed=self.bed,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
            admission_reference=admission.admission_number,
        )
        admission.save(update_fields=("bed_assignment", "updated_at"))
        movement = transfer_patient(
            admission=admission,
            to_unit=self.icu_unit,
            to_bed=self.icu_bed,
            tenant=self.tenant,
            organization=self.organization,
            reason="E2E ICU",
            icu=True,
        )
        admission.refresh_from_db()
        self.bed.refresh_from_db()
        self.icu_bed.refresh_from_db()
        self.assertEqual(movement.movement_type, "icu_transfer")
        self.assertEqual(admission.unit_id, self.icu_unit.pk)
        self.assertEqual(self.bed.status, BedStatus.CLEANING.value)
        self.assertEqual(self.icu_bed.status, BedStatus.OCCUPIED.value)
        discharged = discharge_patient(
            admission=admission, tenant=self.tenant, organization=self.organization
        )
        self.assertEqual(discharged.status, "discharged")
        self.icu_bed.refresh_from_db()
        self.assertEqual(self.icu_bed.status, BedStatus.CLEANING.value)

    def test_cross_tenant_and_organization_access_is_rejected(self):
        other_tenant = _create_root("tenancy.Tenant")
        other_org = _create_root("organizations.Organization", {"tenant": other_tenant})
        other_patient = _create_root(
            "patient_core.Patient", {"tenant": other_tenant, "organization": other_org}
        )
        with self.assertRaises(ValidationError):
            reserve_bed(
                bed=self.bed,
                patient=other_patient,
                tenant=other_tenant,
                organization=other_org,
                reserved_from=timezone.now(),
                reserved_until=timezone.now() + timedelta(hours=1),
            )
        with self.assertRaises(ValidationError):
            reserve_bed(
                bed=self.bed,
                patient=self.patient,
                tenant=other_tenant,
                organization=other_org,
                reserved_from=timezone.now(),
                reserved_until=timezone.now() + timedelta(hours=1),
            )

    def test_active_bed_assignment_database_invariant(self):
        assignment = assign_bed(
            bed=self.bed,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
            admission_reference="E2E-INVARIANT",
        )
        with self.assertRaises((ValidationError, IntegrityError)):
            with transaction.atomic():
                BedAssignment.objects.create(
                    tenant=self.tenant,
                    organization=self.organization,
                    bed=self.bed,
                    patient=self.patient,
                    admission_reference="E2E-DUP",
                    started_at=timezone.now(),
                    active=True,
                )
        self.assertTrue(assignment.active)

    def test_reservation_database_invariant(self):
        reserve_bed(
            bed=self.bed,
            patient=self.patient,
            tenant=self.tenant,
            organization=self.organization,
            reserved_from=timezone.now(),
            reserved_until=timezone.now() + timedelta(hours=1),
        )
        with self.assertRaises((ValidationError, IntegrityError)):
            with transaction.atomic():
                BedReservation.objects.create(
                    tenant=self.tenant,
                    organization=self.organization,
                    bed=self.bed,
                    patient=self.patient,
                    reserved_from=timezone.now(),
                    reserved_until=timezone.now() + timedelta(hours=1),
                    status=ReservationStatus.ACTIVE.value,
                )


class HospitalOperationsRuntimeBoundaryTests(SimpleTestCase):
    def test_cross_domain_adapters_are_callable_without_duplicate_implementations(self):
        from apps.hospital_operations import cross_domain

        for name in (
            "create_encounter",
            "create_laboratory_order",
            "create_imaging_order",
            "create_pharmacy_order",
            "create_rcm_charge",
            "execute_notification",
            "execute_audit",
            "execute_ai",
        ):
            self.assertTrue(callable(getattr(cross_domain, name)))

    def test_workflow_module_does_not_directly_own_external_domain_models(self):
        from apps.hospital_operations.workflow import EXTERNAL_BOUNDARIES

        self.assertEqual(
            set(EXTERNAL_BOUNDARIES),
            {
                "encounter",
                "laboratory",
                "imaging",
                "pharmacy",
                "rcm",
                "notifications",
                "audit",
                "ai",
            },
        )
