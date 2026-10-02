"""
Shared base test cases.

These classes provide reusable test setup shared across
the Datavion AI platform.
"""

from __future__ import annotations

from datetime import (
    date,
    timedelta,
)

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
from apps.clinical.encounters.constants import (
    EncounterStatus,
)
from apps.clinical.encounters.models import Encounter
from apps.clinical.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.clinical.medications.models import Medication
from apps.clinical.providers.constants import ProviderType
from apps.clinical.providers.models import Provider
from apps.organization.departments.models import Department
from apps.organization.employees.models import Employee
from apps.organization.teams.models import Team
from apps.patient_management.patients.constants import PatientGender
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant

User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test case shared across feature applications.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.organization = self.create_organization()

        self.admin = self.create_user(
            username="admin",
            email="admin@datavion.ai",
            password="TestPassword@123",
            organization=self.organization,
            is_staff=True,
            is_superuser=True,
        )

    def create_organization(
        self,
        **kwargs,
    ) -> Organization:
        """
        Create a test organization.
        """

        defaults = {
            "tenant": Tenant.objects.create(
                name="Datavion Test Tenant",
                slug=f"datavion-test-{Tenant.objects.count() + 1}",
            ),
            "name": "Datavion Analytics",
            "code": "DAT",
        }

        defaults.update(kwargs)

        return Organization.objects.create(
            **defaults,
        )

    def create_user(
        self,
        **kwargs,
    ):
        """
        Create a test user.
        """

        password = kwargs.pop(
            "password",
            "TestPassword@123",
        )

        is_superuser = kwargs.pop(
            "is_superuser",
            False,
        )

        defaults = {
            "first_name": "John",
            "last_name": "Doe",
        }

        defaults.update(kwargs)

        if is_superuser:
            return User.objects.create_superuser(
                password=password,
                **defaults,
            )

        return User.objects.create_user(
            password=password,
            **defaults,
        )

    def create_department(
        self,
        **kwargs,
    ) -> Department:
        """
        Create or reuse a test department.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        code = kwargs.pop(
            "code",
            "ENG",
        )

        defaults = {
            "organization": organization,
            "name": "Engineering",
        }

        defaults.update(kwargs)

        department, _ = Department.objects.get_or_create(
            organization=organization,
            code=code,
            defaults=defaults,
        )

        return department

    def create_team(
        self,
        **kwargs,
    ) -> Team:
        """
        Create or reuse a test team.
        """

        department = kwargs.pop("department", None)
        organization = kwargs.pop(
            "organization",
            getattr(department, "organization", self.organization),
        )

        code = kwargs.pop(
            "code",
            "BACKEND",
        )

        defaults = {
            "organization": organization,
            "name": "Backend Team",
        }

        defaults.update(kwargs)

        team, _ = Team.objects.get_or_create(
            organization=organization,
            code=code,
            defaults=defaults,
        )

        return team

    def create_employee(
        self,
        **kwargs,
    ) -> Employee:
        """
        Create or reuse a test employee.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        # Department and team ownership moved to EmployeeAssignment.  Accept
        # these historical factory arguments without writing removed columns.
        kwargs.pop("department", None)
        kwargs.pop("team", None)

        user = kwargs.pop(
            "user",
            None,
        )

        if user is None:
            index = Employee.objects.count() + 1

            user = self.create_user(
                username=f"employee{index}",
                email=f"employee{index}@datavion.ai",
                organization=organization,
            )

        employee_code = kwargs.pop(
            "employee_code",
            f"EMP{Employee.objects.count() + 1:06d}",
        )

        defaults = {
            "user": user,
            "designation": "Software Engineer",
            "joining_date": date(
                2025,
                1,
                1,
            ),
        }

        defaults.update(kwargs)

        employee, _ = Employee.objects.get_or_create(
            organization=organization,
            employee_code=employee_code,
            defaults=defaults,
        )

        return employee

    def create_patient(
        self,
        **kwargs,
    ) -> Patient:
        """
        Create or reuse a test patient.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        mrn = kwargs.pop(
            "mrn",
            f"MRN{Patient.objects.count() + 1:06d}",
        )

        defaults = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(
                1995,
                1,
                1,
            ),
            "gender": PatientGender.MALE,
        }

        defaults.update(kwargs)

        patient, _ = Patient.objects.get_or_create(
            organization=organization,
            mrn=mrn,
            defaults=defaults,
        )

        return patient

    def create_provider(
        self,
        **kwargs,
    ) -> Provider:
        """
        Create or reuse a test provider.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        employee = kwargs.pop(
            "employee",
            None,
        )

        if employee is None:
            employee = self.create_employee(
                organization=organization,
            )

        provider_number = kwargs.pop(
            "provider_number",
            f"PRV{Provider.objects.count() + 1:06d}",
        )

        # Credentials are managed by the provider-credentials bounded context.
        kwargs.pop("license_number", None)

        defaults = {
            "employee": employee,
            "provider_type": ProviderType.PHYSICIAN,
        }

        defaults.update(kwargs)

        provider, _ = Provider.objects.get_or_create(
            organization=organization,
            provider_number=provider_number,
            defaults=defaults,
        )

        return provider

    def create_appointment(
        self,
        **kwargs,
    ) -> Appointment:
        """
        Create a test appointment.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        patient = kwargs.pop(
            "patient",
            self.create_patient(
                organization=organization,
            ),
        )

        provider = kwargs.pop(
            "provider",
            self.create_provider(
                organization=organization,
            ),
        )

        appointment_number = kwargs.pop(
            "appointment_number",
            f"APT{Appointment.objects.count() + 1:06d}",
        )

        defaults = {
            "organization": organization,
            "patient": patient,
            "provider": provider,
            "appointment_number": appointment_number,
            "appointment_type": AppointmentType.CONSULTATION,
            "status": AppointmentStatus.SCHEDULED,
            "priority": AppointmentPriority.NORMAL,
            "scheduled_start": timezone.now(),
            "scheduled_end": timezone.now()
            + timedelta(
                minutes=30,
            ),
            "duration_minutes": 30,
            "reason": "General Consultation",
        }

        defaults.update(kwargs)

        return Appointment.objects.create(
            **defaults,
        )

    def create_encounter(
        self,
        **kwargs,
    ) -> Encounter:
        """
        Create a test encounter.
        """

        organization = kwargs.pop(
            "organization",
            self.organization,
        )

        appointment = kwargs.pop(
            "appointment",
            self.create_appointment(
                organization=organization,
            ),
        )

        patient = kwargs.pop(
            "patient",
            appointment.patient,
        )

        provider = kwargs.pop(
            "provider",
            appointment.provider,
        )

        encounter_number = kwargs.pop(
            "encounter_number",
            f"ENC{Encounter.objects.count() + 1:06d}",
        )

        defaults = {
            "organization": organization,
            "appointment": appointment,
            "patient": patient,
            "provider": provider,
            "encounter_number": encounter_number,
            "status": EncounterStatus.IN_PROGRESS,
            "chief_complaint": "General Consultation",
            "history_of_present_illness": "",
            "assessment": "",
            "plan": "",
            "clinical_notes": "",
            "duration_minutes": 0,
            "is_billable": True,
        }

        defaults.update(kwargs)

        return Encounter.objects.create(
            **defaults,
        )

    def create_medication(
        self,
        **kwargs,
    ) -> Medication:
        """
        Create a medication for tests.
        """

        defaults = {
            "organization": self.organization,
            "medication_code": "MED000001",
            "generic_name": "Paracetamol",
            "brand_name": "Crocin",
            "strength": "500",
            "strength_unit": "mg",
            "dosage_form": MedicationDosageForm.TABLET,
            "route": MedicationRoute.ORAL,
            "manufacturer": "ABC Pharma",
            "description": "Pain reliever",
            "is_controlled": False,
        }

        defaults.update(kwargs)

        return Medication.objects.create(
            **defaults,
        )


class BaseAPITestCase(BaseTestCase):
    """
    Base API test case with an authenticated client.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.client: APIClient = APIClient()
        self.client.defaults["wsgi.url_scheme"] = "https"
        self.client.defaults["SERVER_PORT"] = "443"

        self.client.force_authenticate(
            user=self.admin,
        )


AuthenticatedAPITestCase = BaseAPITestCase

__all__ = (
    "AuthenticatedAPITestCase",
    "BaseAPITestCase",
    "BaseTestCase",
)
