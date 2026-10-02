"""End-to-end Clinical Appointment tests."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import resolve
from django.utils import timezone
from rest_framework.test import APIClient

from apps.clinical.appointments.constants import (
    AppointmentStatus,
    AppointmentType,
)
from apps.clinical.appointments.models import Appointment
from apps.clinical.appointments.services import AppointmentService
from apps.clinical.appointments.workflows import (
    AppointmentBookingRequest,
    AppointmentBookingWorkflow,
    AppointmentCheckInWorkflow,
    AppointmentCompleteWorkflow,
    AppointmentConfirmWorkflow,
    AppointmentDeleteRequest,
    AppointmentDeleteWorkflow,
    AppointmentStartWorkflow,
    AppointmentUpdateRequest,
    AppointmentUpdateWorkflow,
)
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.clinical.medications.models import Medication
from apps.clinical.prescriptions.constants import PrescriptionFrequency
from apps.clinical.prescriptions.models import Prescription
from apps.clinical.prescriptions.services import PrescriptionService
from apps.clinical.providers.models import Provider
from apps.core.workflows import WorkflowContext
from apps.organization.departments.models import Department
from apps.organization.employees.constants import (
    EmploymentStatus,
    EmploymentType,
)
from apps.organization.employees.models import (
    Employee,
    EmployeeAssignment,
)
from apps.organization.teams.models import (
    Team,
    TeamDepartmentAssignment,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class AppointmentEndToEndTests(TestCase):
    """Exercise persistence, workflows, API, lifecycle, and deletion."""

    @classmethod
    def setUpTestData(cls):
        """Build canonical tenant, organization, actor, Patient, and Provider."""

        cls.tenant = Tenant.objects.create(
            name="Appointment E2E Tenant",
            slug="appointment-e2e-tenant",
        )

        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Appointment E2E Organization",
            code="APPT-E2E",
        )

        cls.actor = User.objects.create_superuser(
            username="appointment-e2e-admin",
            email="appointment-e2e-admin@datavion.ai",
            password="TestPassword@123",
            organization=cls.organization,
        )

        department = Department.objects.create(
            organization=cls.organization,
            name="Clinical",
            code="CLINICAL",
        )

        team = Team.objects.create(
            organization=cls.organization,
            name="Primary Care",
            code="PRIMARY",
            description="E2E primary care team.",
            team_type="CLINICAL",
            status="ACTIVE",
            is_active=True,
        )

        TeamDepartmentAssignment.objects.create(
            team=team,
            department=department,
            is_primary=True,
            is_active=True,
        )

        employee_user = User.objects.create_user(
            username="appointment-e2e-provider",
            email="appointment-e2e-provider@datavion.ai",
            password="TestPassword@123",
            organization=cls.organization,
        )

        employee = Employee.objects.create(
            organization=cls.organization,
            user=employee_user,
            employee_code="E2E-EMP-001",
            designation="Physician",
            work_email=employee_user.email,
            phone_number="",
            employment_type=EmploymentType.FULL_TIME,
            status=EmploymentStatus.ACTIVE,
            joining_date=date(2025, 1, 1),
        )

        EmployeeAssignment.objects.create(
            employee=employee,
            department=department,
            team=team,
            supervisor=None,
            effective_from=date(2025, 1, 1),
            is_current=True,
        )

        cls.provider = Provider.objects.create(
            organization=cls.organization,
            employee=employee,
            provider_number="E2E-PROV-001",
            provider_type="physician",
            years_of_experience=5,
            consultation_fee=Decimal("1000.00"),
            bio="End-to-end test provider.",
            is_accepting_patients=True,
            status="active",
        )

        cls.patient = Patient.objects.create(
            organization=cls.organization,
            mrn="E2E-MRN-001",
            first_name="End",
            last_name="Patient",
            date_of_birth=date(1990, 1, 1),
            gender="male",
        )

    def _context(self, name):
        """Build a canonical workflow context."""

        return WorkflowContext(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            workflow_name=name,
            request_id="appointment-e2e",
        )

    def _window(self, days=2):
        """Return a future appointment window."""

        start = timezone.now() + timedelta(
            days=days,
        )
        start = start.replace(
            second=0,
            microsecond=0,
        )

        end = start + timedelta(
            minutes=30,
        )

        return start, end

    def _create_appointment(self, number="E2E-APPT-001"):
        """Create an appointment through the actual booking workflow."""

        start, end = self._window()

        with patch.object(
            AppointmentBookingWorkflow,
            "publish_after_commit",
        ):
            result = AppointmentBookingWorkflow(
                request=AppointmentBookingRequest(
                    organization_id=self.organization.id,
                    patient_id=self.patient.id,
                    provider_id=self.provider.id,
                    scheduled_start=start,
                    scheduled_end=end,
                    data={
                        "appointment_number": number,
                        "appointment_type": AppointmentType.IN_PERSON,
                        "priority": "routine",
                        "duration_minutes": 30,
                        "reason": "E2E consultation",
                        "notes": "E2E test",
                        "is_virtual": False,
                        "meeting_url": "",
                    },
                    actor=self.actor,
                ),
            ).execute(
                context=self._context(
                    "appointment.create",
                ),
            )

        self.assertTrue(
            result.success,
        )

        return result.data

    def test_booking_creates_revenue_cycle_deposit_invoice(self):
        """Booking creates a finalized half-fee invoice in healthcare billing."""

        with patch(
            "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
            return_value=True,
        ):
            appointment = self._create_appointment(
                number="E2E-APPT-DEPOSIT",
            )

        from apps.revenue_cycle.billing.models.healthcare_models import (
            HealthcareInvoice,
        )

        invoice = HealthcareInvoice.objects.get(pk=appointment.deposit_invoice_id)
        self.assertEqual(invoice.total, Decimal("500.00"))
        self.assertEqual(invoice.status, HealthcareInvoice.Status.FINALIZED)
        self.assertEqual(invoice.patient_reference, str(self.patient.pk))

    def test_idempotent_offline_booking_replay_creates_one_appointment_and_invoice(
        self,
    ):
        start, end = self._window(days=4)
        request = AppointmentBookingRequest(
            organization_id=self.organization.id,
            patient_id=self.patient.id,
            provider_id=self.provider.id,
            scheduled_start=start,
            scheduled_end=end,
            data={
                "appointment_number": "E2E-APPT-OFFLINE-REPLAY",
                "appointment_type": AppointmentType.IN_PERSON,
                "priority": "routine",
                "duration_minutes": 30,
                "reason": "",
                "notes": "",
                "is_virtual": False,
                "meeting_url": "",
            },
            actor=self.actor,
            idempotency_key="offline-booking-test-key-001",
        )

        def book():
            with (
                patch(
                    "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
                    return_value=True,
                ),
                patch.object(AppointmentBookingWorkflow, "publish_after_commit"),
            ):
                return AppointmentBookingWorkflow(request=request).execute(
                    context=self._context("appointment.create"),
                )

        first = book()
        replay = book()
        self.assertTrue(first.success)
        self.assertTrue(replay.success)
        self.assertEqual(first.data.pk, replay.data.pk)
        self.assertEqual(first.data.tracking_token, replay.data.tracking_token)

        from apps.revenue_cycle.billing.models.healthcare_models import (
            HealthcareInvoice,
        )

        self.assertEqual(
            HealthcareInvoice.objects.filter(
                claim_reference=f"appointment:{first.data.pk}",
            ).count(),
            1,
        )

    def test_no_show_preserves_paid_deposit_without_refund(self):
        """A missed visit keeps its RCM deposit posted and cannot be marked early."""

        with patch(
            "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
            return_value=True,
        ):
            appointment = self._create_appointment(
                number="E2E-APPT-NO-SHOW",
            )

        from apps.revenue_cycle.billing.healthcare_models import (
            HealthcareInvoice,
            HealthcarePayment,
            HealthcareRefund,
        )
        from apps.revenue_cycle.billing.healthcare_services import (
            post_payment,
        )

        deposit_invoice = HealthcareInvoice.objects.get(
            pk=appointment.deposit_invoice_id,
        )
        post_payment(
            organization=self.organization,
            invoice=deposit_invoice,
            amount=appointment.deposit_amount,
            method=HealthcarePayment.Method.UPI,
            reference="NO-SHOW-DEPOSIT-PAID",
            actor=self.actor,
        )
        appointment.deposit_paid = True
        appointment.save(update_fields=["deposit_paid"])

        with self.assertRaises(ValidationError):
            AppointmentService.transition(
                record=appointment,
                target_status=AppointmentStatus.NO_SHOW,
                actor=self.actor,
            )

        appointment.scheduled_start = timezone.now() - timedelta(hours=2)
        appointment.scheduled_end = timezone.now() - timedelta(hours=1)
        appointment.save(update_fields=["scheduled_start", "scheduled_end"])
        AppointmentService.transition(
            record=appointment,
            target_status=AppointmentStatus.NO_SHOW,
            actor=self.actor,
        )

        deposit_invoice.refresh_from_db()
        self.assertEqual(appointment.status, AppointmentStatus.NO_SHOW)
        self.assertEqual(deposit_invoice.paid_total, appointment.deposit_amount)
        self.assertFalse(
            HealthcareRefund.objects.filter(
                organization=self.organization,
                payment__invoice=deposit_invoice,
            ).exists(),
        )

    def test_last_doctor_verified_prescription_auto_checks_out(self):
        """Auto-complete the encounter and appointment after all prescriptions are verified."""

        with patch(
            "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
            return_value=True,
        ):
            appointment = self._create_appointment(
                number="E2E-APPT-RX-VERIFY",
            )
        appointment.status = AppointmentStatus.IN_PROGRESS
        appointment.save(update_fields=["status"])
        encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="E2E-ENC-RX-VERIFY",
            status=EncounterStatus.IN_PROGRESS,
        )
        medication = Medication.objects.create(
            organization=self.organization,
            medication_code="E2E-MED-RX-VERIFY",
            generic_name="Test medication",
            strength="10",
            strength_unit="mg",
            dosage_form=MedicationDosageForm.TABLET,
            route=MedicationRoute.ORAL,
        )
        doctor = self.provider.employee.user
        prescriptions = [
            Prescription.objects.create(
                organization=self.organization,
                patient=self.patient,
                provider=self.provider,
                encounter=encounter,
                medication=medication,
                prescription_number=f"E2E-RX-VERIFY-{index}",
                dosage=1,
                dosage_unit="tablet",
                frequency=PrescriptionFrequency.ONCE_DAILY,
                quantity=1,
                duration_days=1,
                start_date=date.today(),
                end_date=date.today(),
            )
            for index in (1, 2)
        ]

        PrescriptionService.transition(
            organization=self.organization,
            record_id=prescriptions[0].pk,
            target="verify",
            performed_by=doctor,
        )
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, AppointmentStatus.IN_PROGRESS)

        PrescriptionService.transition(
            organization=self.organization,
            record_id=prescriptions[1].pk,
            target="verify",
            performed_by=doctor,
        )
        appointment.refresh_from_db()
        encounter.refresh_from_db()
        self.assertEqual(appointment.status, AppointmentStatus.COMPLETED)
        self.assertIsNotNone(appointment.check_out_at)
        self.assertEqual(encounter.status, EncounterStatus.COMPLETED)

    def test_workflow_crud_and_lifecycle(self):
        """Exercise create, update, confirm, check-in, start, complete, and delete."""

        with (
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
                return_value=True,
            ),
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_update",
                return_value=True,
            ),
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_transition",
                return_value=True,
            ),
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_delete",
                return_value=True,
            ),
        ):
            appointment = self._create_appointment()
            appointment.deposit_paid = True
            appointment.save(update_fields=["deposit_paid"])

            update_result = AppointmentUpdateWorkflow(
                request=AppointmentUpdateRequest(
                    organization_id=self.organization.id,
                    appointment_id=appointment.id,
                    data={
                        "notes": "Updated by E2E workflow.",
                    },
                    actor=self.actor,
                ),
            ).execute(
                context=self._context(
                    "appointment.update",
                ),
            )

            self.assertTrue(
                update_result.success,
            )
            self.assertEqual(
                update_result.data.notes,
                "Updated by E2E workflow.",
            )

            for workflow, name, expected_status in (
                (
                    AppointmentConfirmWorkflow,
                    "appointment.confirm",
                    AppointmentStatus.CONFIRMED,
                ),
                (
                    AppointmentCheckInWorkflow,
                    "appointment.check_in",
                    AppointmentStatus.CHECKED_IN,
                ),
                (
                    AppointmentStartWorkflow,
                    "appointment.start",
                    AppointmentStatus.IN_PROGRESS,
                ),
                (
                    AppointmentCompleteWorkflow,
                    "appointment.complete",
                    AppointmentStatus.COMPLETED,
                ),
            ):
                result = workflow(
                    organization_id=self.organization.id,
                    appointment_id=appointment.id,
                    actor=self.actor,
                ).execute(
                    context=self._context(name),
                )

                self.assertTrue(
                    result.success,
                )

                appointment.refresh_from_db()

                self.assertEqual(
                    appointment.status,
                    expected_status,
                )

            self.assertIsNotNone(
                appointment.check_in_at,
            )
            from apps.revenue_cycle.billing.models.healthcare_models import (
                HealthcareInvoice,
            )

            visit_invoice = HealthcareInvoice.objects.get(
                pk=appointment.final_invoice_id,
            )
            self.assertEqual(visit_invoice.total, Decimal("1000.00"))
            self.assertEqual(visit_invoice.adjustment_total, Decimal("-500.00"))
            self.assertEqual(visit_invoice.balance_due, Decimal("500.00"))
            self.assertIsNotNone(
                appointment.check_out_at,
            )

        with patch(
            "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
            return_value=True,
        ):
            deleted_appointment = self._create_appointment(
                number="E2E-APPT-DELETE",
            )

        with (
            patch.object(
                AppointmentDeleteWorkflow,
                "publish_after_commit",
            ),
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_delete",
                return_value=True,
            ),
        ):
            delete_result = AppointmentDeleteWorkflow(
                request=AppointmentDeleteRequest(
                    organization_id=self.organization.id,
                    appointment_id=deleted_appointment.id,
                    actor=self.actor,
                ),
            ).execute(
                context=self._context(
                    "appointment.delete",
                ),
            )

        self.assertTrue(
            delete_result.success,
        )

        deleted_appointment.refresh_from_db()

        self.assertTrue(
            deleted_appointment.is_deleted,
        )
        self.assertFalse(
            deleted_appointment.is_active,
        )

    def test_api_crud_and_routes(self):
        """Exercise real API URLs through DRF's test client."""

        client = APIClient()
        client.force_authenticate(
            user=self.actor,
        )

        collection_url = "/api/appointments/"

        with (
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
                return_value=True,
            ),
            patch.object(
                AppointmentBookingWorkflow,
                "publish_after_commit",
            ),
        ):
            start, end = self._window(
                days=3,
            )

            response = client.post(
                collection_url,
                {
                    "appointment_number": "E2E-APPT-API",
                    "patient_id": str(self.patient.id),
                    "provider_id": str(self.provider.id),
                    "appointment_type": "in_person",
                    "priority": "routine",
                    "scheduled_start": start.isoformat(),
                    "scheduled_end": end.isoformat(),
                    "duration_minutes": 30,
                    "reason": "API E2E",
                    "notes": "API create",
                    "is_virtual": False,
                    "meeting_url": "",
                },
                format="json",
            )

        self.assertEqual(
            response.status_code,
            201,
        )
        self.assertTrue(response.data["success"])

        appointment_id = response.data["data"]["id"]
        tracking_token = response.data["data"]["tracking_token"]

        client.force_authenticate(user=None)
        tracking_response = client.get(
            f"{collection_url}track/{tracking_token}/",
        )
        self.assertEqual(tracking_response.status_code, 200)
        self.assertEqual(
            tracking_response.data["data"]["appointment_number"],
            "E2E-APPT-API",
        )
        self.assertNotIn("patient", tracking_response.data["data"])
        client.force_authenticate(user=self.actor)

        response = client.get(
            f"{collection_url}{appointment_id}/",
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTrue(response.data["success"])

        with (
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_update",
                return_value=True,
            ),
            patch.object(
                AppointmentUpdateWorkflow,
                "publish_after_commit",
            ),
        ):
            response = client.patch(
                f"{collection_url}{appointment_id}/",
                {
                    "notes": "API updated",
                },
                format="json",
            )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTrue(response.data["success"])

        with (
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_transition",
                return_value=True,
            ),
            patch(
                "apps.clinical.appointments.workflows.appointment.AppointmentStatusChanged",
            ),
            patch.object(
                AppointmentConfirmWorkflow,
                "publish_after_commit",
            ),
        ):
            response = client.post(
                f"{collection_url}{appointment_id}/confirm/",
                {},
                format="json",
            )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data["data"]["status"],
            AppointmentStatus.CONFIRMED,
        )

        match = resolve(
            f"{collection_url}{appointment_id}/confirm/",
        )

        self.assertEqual(
            match.url_name,
            "appointment-confirm",
        )

        self.assertTrue(
            Appointment.objects.filter(
                id=appointment_id,
                organization=self.organization,
            ).exists(),
        )

    def test_reschedule_is_once_and_next_day_only(self):
        """Allow one next-day reschedule and reject later changes."""

        with patch(
            "apps.clinical.appointments.workflows.appointment.AppointmentPolicy.can_create",
            return_value=True,
        ):
            appointment = self._create_appointment(
                number="E2E-APPT-RESCHEDULE",
            )

        tomorrow = timezone.now() + timedelta(days=1)
        next_day_start = tomorrow.replace(second=0, microsecond=0)
        next_day_end = next_day_start + timedelta(minutes=30)

        AppointmentService.reschedule(
            record=appointment,
            scheduled_start=next_day_start,
            scheduled_end=next_day_end,
            duration_minutes=30,
        )

        appointment.refresh_from_db()
        self.assertEqual(appointment.reschedule_count, 1)
        self.assertFalse(appointment.can_reschedule)

        with self.assertRaises(ValidationError):
            AppointmentService.reschedule(
                record=appointment,
                scheduled_start=next_day_start + timedelta(days=1),
                scheduled_end=next_day_end + timedelta(days=1),
                duration_minutes=30,
            )


__all__ = ("AppointmentEndToEndTests",)
