from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.clinical.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
)
from apps.clinical.appointments.models import Appointment
from apps.clinical.diagnoses.constants import DiagnosisStatus, DiagnosisType
from apps.clinical.diagnoses.models import Diagnosis
from apps.clinical.diagnoses.workflows import (
    DiagnosisCreateRequest,
    DiagnosisCreateWorkflow,
    DiagnosisDeleteRequest,
    DiagnosisDeleteWorkflow,
    DiagnosisUpdateRequest,
    DiagnosisUpdateWorkflow,
)
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.clinical.providers.models import Provider
from apps.organization.departments.models import Department
from apps.organization.employees.constants import EmploymentStatus, EmploymentType
from apps.organization.employees.models import Employee, EmployeeAssignment
from apps.organization.teams.models import Team, TeamDepartmentAssignment
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant

User = get_user_model()


class PolicyStub:
    def can_create(self, **kwargs):
        return True

    def can_update(self, **kwargs):
        return True

    def can_delete(self, **kwargs):
        return True


class DiagnosisEndToEndTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            name="Datavion Diagnosis E2E Tenant",
            slug="datavion-diagnosis-e2e-tenant",
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Diagnosis E2E Organization",
            code="DX-E2E",
        )
        cls.user = User.objects.create_user(
            username="diagnosis-e2e",
            email="diagnosis-e2e@datavion.ai",
            password="TestPassword@123",
            organization=cls.organization,
        )
        department = Department.objects.create(
            organization=cls.organization,
            name="Primary Care",
            code="DXPC",
        )
        team = Team.objects.create(
            organization=cls.organization,
            name="Primary Care",
            code="DXTEAM",
            description="Diagnosis E2E",
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
        employee = Employee.objects.create(
            organization=cls.organization,
            user=cls.user,
            employee_code="DX-E2E-EMP",
            designation="Physician",
            work_email=cls.user.email,
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
            provider_number="DX-E2E-PROV",
            provider_type="physician",
            years_of_experience=5,
            bio="Diagnosis E2E",
            is_accepting_patients=True,
            status="active",
        )
        cls.patient = Patient.objects.create(
            organization=cls.organization,
            mrn="DX-E2E-MRN",
            first_name="Diagnosis",
            last_name="Patient",
            date_of_birth=date(1990, 1, 1),
            gender="male",
        )
        cls.appointment = Appointment.objects.create(
            organization=cls.organization,
            patient=cls.patient,
            provider=cls.provider,
            appointment_number="DX-E2E-APT",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
            priority=AppointmentPriority.ROUTINE,
            scheduled_start=timezone.now() + timedelta(hours=1),
            scheduled_end=timezone.now() + timedelta(hours=1, minutes=30),
            duration_minutes=30,
            reason="Diagnosis E2E",
        )
        cls.encounter = Encounter.objects.create(
            organization=cls.organization,
            appointment=cls.appointment,
            patient=cls.patient,
            provider=cls.provider,
            encounter_number="DX-E2E-ENC",
            status=EncounterStatus.SCHEDULED,
        )

    def context(self, name):
        from apps.core.workflows import WorkflowContext

        return WorkflowContext(
            tenant_id=self.organization.tenant_id,
            actor_id=self.user.pk,
            workflow_name=name,
        )

    def test_workflow_crud(self):
        with (
            patch(
                "apps.platform.rbac.permissions.base.user_has_permission",
                return_value=True,
            ) as rbac_check,
            patch(
                "apps.clinical.diagnoses.workflows.diagnosis.DiagnosisPolicy",
                return_value=PolicyStub(),
            ),
        ):
            created = DiagnosisCreateWorkflow(
                request=DiagnosisCreateRequest(
                    organization_id=self.organization.id,
                    encounter_id=self.encounter.id,
                    diagnosis_code="J06.9",
                    diagnosis_type=DiagnosisType.PRIMARY,
                    data={
                        "diagnosis_description": "Acute upper respiratory infection",
                        "is_primary": True,
                        "present_on_admission": True,
                    },
                )
            ).execute(context=self.context("diagnosis.create"))
            self.assertTrue(created.success)
            diagnosis = created.data
            self.assertEqual(diagnosis.status, DiagnosisStatus.ACTIVE)

            updated = DiagnosisUpdateWorkflow(
                request=DiagnosisUpdateRequest(
                    organization_id=self.organization.id,
                    diagnosis_id=diagnosis.id,
                    data={"notes": "Confirmed clinically"},
                )
            ).execute(context=self.context("diagnosis.update"))
            self.assertTrue(updated.success)

            second = DiagnosisCreateWorkflow(
                request=DiagnosisCreateRequest(
                    organization_id=self.organization.id,
                    encounter_id=self.encounter.id,
                    diagnosis_code="R05.9",
                    diagnosis_type=DiagnosisType.SECONDARY,
                    data={"diagnosis_description": "Cough"},
                )
            ).execute(context=self.context("diagnosis.create"))
            deleted = DiagnosisDeleteWorkflow(
                request=DiagnosisDeleteRequest(
                    organization_id=self.organization.id,
                    diagnosis_id=second.data.id,
                )
            ).execute(context=self.context("diagnosis.delete"))
            self.assertTrue(deleted.success)
            record = Diagnosis.all_objects.get(pk=second.data.id)
            self.assertTrue(record.is_deleted)
            self.assertFalse(record.is_active)

    def test_api_crud_and_routes(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        client.credentials(HTTP_X_ORGANIZATION_ID=str(self.organization.id))
        with (
            patch(
                "apps.platform.rbac.permissions.base.user_has_permission",
                return_value=True,
            ) as rbac_check,
            patch(
                "apps.clinical.diagnoses.workflows.diagnosis.DiagnosisPolicy",
                return_value=PolicyStub(),
            ),
        ):
            response = client.post(
                "/api/diagnoses/",
                {
                    "encounter": str(self.encounter.id),
                    "diagnosis_code": "E11.9",
                    "diagnosis_description": "Type 2 diabetes mellitus",
                    "diagnosis_type": DiagnosisType.SECONDARY,
                    "is_primary": False,
                    "present_on_admission": None,
                    "notes": "API test",
                },
                format="json",
            )
            rbac_check.assert_called()
            self.assertEqual(response.status_code, 201, response.data)
            diagnosis_id = response.data["id"]
            self.assertEqual(
                client.get(f"/api/diagnoses/{diagnosis_id}/").status_code, 200
            )
            self.assertEqual(
                client.patch(
                    f"/api/diagnoses/{diagnosis_id}/",
                    {"notes": "Updated"},
                    format="json",
                ).status_code,
                200,
            )
            self.assertEqual(
                client.delete(f"/api/diagnoses/{diagnosis_id}/").status_code,
                200,
            )
