"""
Shared base test cases.

These classes provide reusable test setup shared across
the Datavion AI platform.
"""

from __future__ import annotations
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from apps.departments.models import Department
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.patients.constants import PatientGender
from apps.patients.models import Patient
from apps.providers.constants import ProviderType
from apps.providers.models import Provider
from apps.teams.models import Team
from datetime import (
    date,
    timedelta,
)
from django.utils import timezone
from apps.appointments.constants import (
    AppointmentPriority,
    AppointmentStatus,
    AppointmentType,
)
from apps.appointments.models import Appointment
User = get_user_model()
from apps.encounters.constants import (
    EncounterStatus,
)
from apps.encounters.models import Encounter


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

        department = kwargs.pop(
            "department",
            self.create_department(),
        )

        code = kwargs.pop(
            "code",
            "BACKEND",
        )

        defaults = {
            "department": department,
            "name": "Backend Team",
        }

        defaults.update(kwargs)

        team, _ = Team.objects.get_or_create(
            department=department,
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

        department = kwargs.pop(
            "department",
            None,
        )

        if department is None:
            department = self.create_department(
                organization=organization,
            )

        team = kwargs.pop(
            "team",
            None,
        )

        if team is None:
            team = self.create_team(
                department=department,
            )

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
            "department": department,
            "team": team,
            "user": user,
            "designation": "Software Engineer",
            "hire_date": date(
                2025,
                1,
                1,
            ),
            "is_active": True,
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

        license_number = kwargs.pop(
            "license_number",
            f"LIC{Provider.objects.count() + 1:06d}",
        )

        defaults = {
            "employee": employee,
            "provider_type": ProviderType.PHYSICIAN,
        }

        defaults.update(kwargs)

        provider, _ = Provider.objects.get_or_create(
            organization=organization,
            provider_number=provider_number,
            defaults={
                **defaults,
                "license_number": license_number,
            },
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
            "scheduled_end": timezone.now() + timedelta(
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

class BaseAPITestCase(BaseTestCase):
    """
    Base API test case with an authenticated client.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.client = APIClient()

        self.client.force_authenticate(
            user=self.admin,
        )
