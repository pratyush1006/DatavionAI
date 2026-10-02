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
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.clinical.encounters.workflows import (
    EncounterCompleteWorkflow,
    EncounterCreateRequest,
    EncounterCreateWorkflow,
    EncounterDeleteWorkflow,
    EncounterLifecycleRequest,
    EncounterStartWorkflow,
    EncounterUpdateRequest,
    EncounterUpdateWorkflow,
)
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

    def can_transition(self, **kwargs):
        return True

    def can_view(self, **kwargs):
        return True


class EncounterEndToEndTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            name="Datavion Encounter E2E Tenant",
            slug="datavion-encounter-e2e-tenant",
        )
        cls.organization = Organization.objects.create(
            tenant=cls.tenant,
            name="Encounter E2E Organization",
            code="ENC-E2E",
        )
        cls.user = User.objects.create_user(
            username="encounter-e2e",
            email="encounter-e2e@datavion.ai",
            password="TestPassword@123",
            organization=cls.organization,
        )
        department = Department.objects.create(
            organization=cls.organization,
            name="Primary Care",
            code="ENCPC",
        )
        team = Team.objects.create(
            organization=cls.organization,
            name="Primary Care",
            code="ENCTEAM",
            description="Encounter E2E",
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
            employee_code="ENC-E2E-EMP",
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
            provider_number="ENC-E2E-PROV",
            provider_type="physician",
            years_of_experience=5,
            bio="Encounter E2E",
            is_accepting_patients=True,
            status="active",
        )
        cls.patient = Patient.objects.create(
            organization=cls.organization,
            mrn="ENC-E2E-MRN",
            first_name="Encounter",
            last_name="Patient",
            date_of_birth=date(1990, 1, 1),
            gender="male",
        )
        cls.appointment = Appointment.objects.create(
            organization=cls.organization,
            patient=cls.patient,
            provider=cls.provider,
            appointment_number="ENC-E2E-APT",
            appointment_type=AppointmentType.CONSULTATION,
            status=AppointmentStatus.SCHEDULED,
            priority=AppointmentPriority.ROUTINE,
            scheduled_start=timezone.now() + timedelta(hours=1),
            scheduled_end=timezone.now() + timedelta(hours=1, minutes=30),
            duration_minutes=30,
            reason="Encounter E2E",
        )

    def context(self, name):
        from apps.core.workflows import WorkflowContext

        return WorkflowContext(
            tenant_id=self.organization.tenant_id,
            actor_id=self.user.pk,
            workflow_name=name,
        )

    def test_workflow_crud_and_lifecycle(self):
        with (
            patch(
                "apps.platform.rbac.permissions.base.user_has_permission",
                return_value=True,
            ) as rbac_check,
            patch(
                "apps.clinical.encounters.workflows.encounter.EncounterPolicy",
                return_value=PolicyStub(),
            ),
        ):
            created = EncounterCreateWorkflow(
                request=EncounterCreateRequest(
                    organization_id=self.organization.id,
                    appointment_id=self.appointment.id,
                    patient_id=self.patient.id,
                    provider_id=self.provider.id,
                    encounter_number="ENC-E2E-001",
                    data={"chief_complaint": "Cough"},
                )
            ).execute(context=self.context("encounter.create"))
            self.assertTrue(created.success)
            encounter = created.data

            updated = EncounterUpdateWorkflow(
                request=EncounterUpdateRequest(
                    organization_id=self.organization.id,
                    encounter_id=encounter.id,
                    data={"assessment": "Viral URI"},
                )
            ).execute(context=self.context("encounter.update"))
            self.assertTrue(updated.success)

            started = EncounterStartWorkflow(
                request=EncounterLifecycleRequest(
                    organization_id=self.organization.id,
                    encounter_id=encounter.id,
                )
            ).execute(context=self.context("encounter.start"))
            self.assertEqual(started.data.status, EncounterStatus.IN_PROGRESS)

            completed = EncounterCompleteWorkflow(
                request=EncounterLifecycleRequest(
                    organization_id=self.organization.id,
                    encounter_id=encounter.id,
                )
            ).execute(context=self.context("encounter.complete"))
            self.assertEqual(completed.data.status, EncounterStatus.COMPLETED)

            appointment = Appointment.objects.create(
                organization=self.organization,
                patient=self.patient,
                provider=self.provider,
                appointment_number="ENC-E2E-APT-2",
                appointment_type=AppointmentType.CONSULTATION,
                status=AppointmentStatus.SCHEDULED,
                priority=AppointmentPriority.ROUTINE,
                scheduled_start=timezone.now() + timedelta(hours=2),
                scheduled_end=timezone.now() + timedelta(hours=2, minutes=30),
                duration_minutes=30,
                reason="Delete",
            )
            second = EncounterCreateWorkflow(
                request=EncounterCreateRequest(
                    organization_id=self.organization.id,
                    appointment_id=appointment.id,
                    patient_id=self.patient.id,
                    provider_id=self.provider.id,
                    encounter_number="ENC-E2E-002",
                    data={},
                )
            ).execute(context=self.context("encounter.create"))
            deleted = EncounterDeleteWorkflow(
                request=EncounterLifecycleRequest(
                    organization_id=self.organization.id,
                    encounter_id=second.data.id,
                )
            ).execute(context=self.context("encounter.delete"))
            self.assertTrue(deleted.success)
            record = Encounter.all_objects.get(pk=second.data.id)
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
                "apps.clinical.encounters.workflows.encounter.EncounterPolicy",
                return_value=PolicyStub(),
            ),
        ):
            response = client.post(
                "/api/encounters/",
                {
                    "appointment": str(self.appointment.id),
                    "patient": str(self.patient.id),
                    "provider": str(self.provider.id),
                    "encounter_number": "ENC-E2E-API",
                    "chief_complaint": "Headache",
                    "is_billable": True,
                },
                format="json",
            )
            rbac_check.assert_called()
            self.assertEqual(response.status_code, 201, response.data)
            encounter_id = response.data["id"]
            self.assertEqual(
                client.get(f"/api/encounters/{encounter_id}/").status_code,
                200,
            )
            self.assertEqual(
                client.patch(
                    f"/api/encounters/{encounter_id}/",
                    {"assessment": "Stable"},
                    format="json",
                ).status_code,
                200,
            )
            self.assertEqual(
                client.post(
                    f"/api/encounters/{encounter_id}/start/",
                    {},
                    format="json",
                ).status_code,
                200,
            )
            self.assertEqual(
                client.post(
                    f"/api/encounters/{encounter_id}/complete/",
                    {},
                    format="json",
                ).status_code,
                200,
            )
            self.assertEqual(
                Encounter.objects.get(pk=encounter_id).status,
                EncounterStatus.COMPLETED,
            )

    @patch(
        "apps.clinical.encounters.workflows.encounter.EncounterPolicy",
        return_value=PolicyStub(),
    )
    def test_encounter_lifecycle_queues_insurance_and_coding_work(self, _policy):
        from apps.insurance.constants import CoverageStatus
        from apps.insurance.models import Enrollment, InsurancePlan, Payer
        from apps.revenue_cycle.coding.constants import CodingStatus
        from apps.revenue_cycle.coding.models import CodingRecord
        from apps.revenue_cycle.insurance_verification.constants import (
            VerificationMethod,
            VerificationOutcome,
            VerificationStatus,
        )
        from apps.revenue_cycle.insurance_verification.models import (
            InsuranceVerification,
        )

        payer = Payer.objects.create(
            organization=self.organization,
            legal_name="Encounter workflow payer",
            display_name="Encounter workflow payer",
            payer_code="ENC-WORKFLOW-PAYER",
        )
        plan = InsurancePlan.objects.create(
            organization=self.organization,
            payer=payer,
            name="Encounter workflow plan",
            plan_code="ENC-WORKFLOW-PLAN",
        )
        Enrollment.objects.create(
            organization=self.organization,
            patient=self.patient,
            plan=plan,
            member_id="ENC-WORKFLOW-MEMBER",
            policy_number="ENC-WORKFLOW-POLICY",
            group_number="ENC-WORKFLOW-GROUP",
            effective_date=date.today() - timedelta(days=30),
            status=CoverageStatus.ACTIVE,
            is_primary=True,
        )

        with self.captureOnCommitCallbacks(execute=True):
            created = EncounterCreateWorkflow(
                request=EncounterCreateRequest(
                    organization_id=self.organization.id,
                    appointment_id=self.appointment.id,
                    patient_id=self.patient.id,
                    provider_id=self.provider.id,
                    encounter_number="ENC-INSURANCE-WORKFLOW",
                    data={
                        "chief_complaint": "Cough",
                        "assessment": "Upper respiratory symptoms",
                    },
                )
            ).execute(context=self.context("encounter.create"))

        self.assertTrue(created.success)
        encounter = created.data
        request_reference = (
            f"encounter:{encounter.id}:enrollment:"
            f"{Enrollment.objects.get(patient=self.patient).id}"
        )
        verification = InsuranceVerification.objects.get(
            organization=self.organization,
            patient=self.patient,
            request_reference=request_reference,
        )
        self.assertEqual(verification.status, VerificationStatus.PENDING)
        self.assertEqual(verification.outcome, VerificationOutcome.UNKNOWN)
        self.assertEqual(verification.verification_method, VerificationMethod.MANUAL)
        self.assertEqual(
            verification.response_payload["encounter_id"],
            str(encounter.id),
        )
        self.assertIn("still required", verification.response_message)

        with self.captureOnCommitCallbacks(execute=True):
            started = EncounterStartWorkflow(
                request=EncounterLifecycleRequest(
                    organization_id=self.organization.id,
                    encounter_id=encounter.id,
                )
            ).execute(context=self.context("encounter.start"))
        self.assertEqual(started.data.status, EncounterStatus.IN_PROGRESS)
        self.assertFalse(
            CodingRecord.objects.filter(
                organization=self.organization,
                source_reference=str(encounter.id),
            ).exists()
        )

        with self.captureOnCommitCallbacks(execute=True):
            completed = EncounterCompleteWorkflow(
                request=EncounterLifecycleRequest(
                    organization_id=self.organization.id,
                    encounter_id=encounter.id,
                )
            ).execute(context=self.context("encounter.complete"))

        self.assertEqual(completed.data.status, EncounterStatus.COMPLETED)
        coding = CodingRecord.objects.get(
            organization=self.organization,
            patient=self.patient,
            source_reference=str(encounter.id),
        )
        self.assertEqual(coding.status, CodingStatus.DRAFT)
        self.assertEqual(coding.clinical_summary, "Cough\n\nUpper respiratory symptoms")
        self.assertEqual(
            coding.documentation["encounter_number"], encounter.encounter_number
        )
