from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.clinical.appointments.models import Appointment
from apps.clinical.encounters.models import Encounter
from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.clinical.medications.models import Medication
from apps.clinical.prescriptions.models import Prescription
from apps.clinical.providers.constants import ProviderType
from apps.clinical.providers.models import Provider
from apps.hospital_operations.models import Facility, OperationalUnit
from apps.organization.employees.models import Employee
from apps.patient_management.patients.constants import PatientGender
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


@override_settings(
    ROOT_URLCONF="apps.clinical.nursing.tests.urls",
    SECURE_SSL_REDIRECT=False,
)
class NursingEndToEndTests(APITestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Nursing Tenant", slug="nursing-tenant"
        )
        self.organization = Organization.objects.create(
            tenant=self.tenant, name="Nursing Hospital", code="NURSING-HOSPITAL"
        )
        User = get_user_model()
        self.user = User.objects.create_user(
            email="nurse@example.test",
            password="password",
            is_superuser=True,
            is_staff=True,
        )
        self.incoming_user = User.objects.create_user(
            email="incoming@example.test",
            password="password",
            is_superuser=True,
            is_staff=True,
        )
        self.nurse = self._provider(self.user, "NURSE-1")
        self.incoming = self._provider(self.incoming_user, "NURSE-2")
        self.patient = Patient.objects.create(
            organization=self.organization,
            mrn="MRN-NURSE-1",
            first_name="Patient",
            last_name="One",
            date_of_birth=date(1990, 1, 1),
            gender=PatientGender.FEMALE,
        )
        self.facility = Facility.objects.create(
            tenant=self.tenant, organization=self.organization, name="Main", code="MAIN"
        )
        self.ward = OperationalUnit.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            facility=self.facility,
            name="Ward A",
            code="WARD-A",
        )
        start = timezone.now() + timedelta(hours=1)
        appointment = Appointment.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.nurse,
            appointment_number="APT-NURSING",
            scheduled_start=start,
            scheduled_end=start + timedelta(minutes=30),
        )
        encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=appointment,
            patient=self.patient,
            provider=self.nurse,
            encounter_number="ENC-NURSING",
        )
        medication = Medication.objects.create(
            organization=self.organization,
            medication_code="MED-NURSING",
            generic_name="Paracetamol",
            strength="500",
            strength_unit="mg",
            dosage_form=MedicationDosageForm.TABLET,
            route=MedicationRoute.ORAL,
        )
        self.prescription = Prescription.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.nurse,
            encounter=encounter,
            medication=medication,
            prescription_number="RX-NURSING",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
        )
        self.client.force_authenticate(self.user)
        self.client.credentials(
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
            HTTP_X_TENANT_ID=str(self.tenant.id),
        )

    def _provider(self, user, code):
        employee = Employee.objects.create(
            organization=self.organization,
            user=user,
            employee_code=code,
            designation="Nurse",
            joining_date=date.today(),
        )
        return Provider.objects.create(
            organization=self.organization,
            employee=employee,
            provider_number=code,
            provider_type=ProviderType.NURSE,
        )

    def post(self, path, data):
        response = self.client.post(f"/api/nursing/{path}", data, format="json")
        self.assertIn(response.status_code, (200, 201), response.data)
        return response.data.get("data", response.data)

    def test_complete_nursing_workflow(self):
        now = timezone.now()
        assignment = self.post(
            "assignments/",
            {
                "patient": str(self.patient.id),
                "nurse": str(self.nurse.id),
                "ward": str(self.ward.uuid),
                "started_at": now.isoformat(),
            },
        )
        task = self.post(
            "tasks/",
            {
                "patient": str(self.patient.id),
                "assigned_nurse": str(self.nurse.id),
                "assignment": assignment["id"],
                "title": "Record observations",
                "task_type": "vitals",
                "priority": "urgent",
                "due_at": (now + timedelta(hours=1)).isoformat(),
            },
        )
        self.post(f"tasks/{task['id']}/start/", {})
        completed = self.post(
            f"tasks/{task['id']}/complete/",
            {"completion_notes": "Observations recorded"},
        )
        self.assertEqual(completed["status"], "completed")
        administration = self.post(
            "medication-administrations/",
            {
                "patient": str(self.patient.id),
                "prescription": str(self.prescription.id),
                "nurse": str(self.nurse.id),
                "scheduled_at": now.isoformat(),
                "dose": "500 mg",
                "route": "oral",
            },
        )
        administered = self.post(
            f"medication-administrations/{administration['id']}/administer/",
            {"notes": "Given after food"},
        )
        self.assertEqual(administered["status"], "administered")
        plan = self.post(
            "care-plans/",
            {
                "patient": str(self.patient.id),
                "primary_nurse": str(self.nurse.id),
                "title": "Pain management",
                "goals": ["Pain below 3"],
                "interventions": ["Assess every four hours"],
            },
        )
        active_plan = self.post(f"care-plans/{plan['id']}/activate/", {})
        self.assertEqual(active_plan["status"], "active")
        alert = self.post(
            "alerts/",
            {
                "patient": str(self.patient.id),
                "assigned_nurse": str(self.nurse.id),
                "title": "Low oxygen",
                "message": "Oxygen saturation below threshold",
                "severity": "critical",
            },
        )
        self.post(f"alerts/{alert['id']}/acknowledge/", {})
        self.post(
            f"alerts/{alert['id']}/escalate/", {"escalated_to": str(self.incoming.id)}
        )
        resolved = self.post(
            f"alerts/{alert['id']}/resolve/", {"resolution_notes": "Patient stabilized"}
        )
        self.assertEqual(resolved["status"], "resolved")
        schedule = self.post(
            "schedules/",
            {
                "nurse": str(self.nurse.id),
                "ward": str(self.ward.uuid),
                "starts_at": now.isoformat(),
                "ends_at": (now + timedelta(hours=8)).isoformat(),
                "shift_type": "morning",
            },
        )
        self.post(f"schedules/{schedule['id']}/start/", {})
        handover = self.post(
            "handovers/",
            {
                "schedule": schedule["id"],
                "from_nurse": str(self.nurse.id),
                "to_nurse": str(self.incoming.id),
                "ward": str(self.ward.uuid),
                "patients": [str(self.patient.id)],
                "summary": "Stable after intervention",
                "outstanding_tasks": ["Repeat observations"],
            },
        )
        self.post(f"handovers/{handover['id']}/submit/", {})
        self.client.force_authenticate(self.incoming_user)
        accepted = self.post(f"handovers/{handover['id']}/accept/", {})
        self.assertEqual(accepted["status"], "accepted")
        ended = self.post(f"assignments/{assignment['id']}/end/", {})
        self.assertEqual(ended["status"], "ended")
