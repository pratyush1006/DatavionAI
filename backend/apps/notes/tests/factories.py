"""
Factories for Notes tests.
"""

from __future__ import annotations

from datetime import date

import factory
from django.contrib.auth import get_user_model

from apps.clinical.patients.tests.factories import PatientFactory
from apps.notes.constants import NoteType, TemplateType
from apps.notes.models import ClinicalNote, NoteTemplate
from apps.organization.departments.models import Department
from apps.organization.employees.models import Employee
from apps.organization.teams.models import Team
from apps.platform.organizations.tests.factories.organization import (
    OrganizationFactory,
)

User = get_user_model()


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Factory for Employee model.
    """

    class Meta:
        model = Employee

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    department = factory.LazyAttribute(
        lambda obj: Department.objects.get_or_create(
            organization=obj.organization,
            name="Test Department",
            code="TEST",
        )[0],
    )

    team = factory.LazyAttribute(
        lambda obj: Team.objects.get_or_create(
            department=obj.department,
            name="Test Team",
            code="TEST",
        )[0],
    )

    user = factory.LazyAttribute(
        lambda obj: User.objects.get_or_create(
            username=f"employee_{obj.employee_code}",
            defaults={
                "email": f"employee_{obj.employee_code}@test.com",
                "password": "testpass123",
                "first_name": "Test",
                "last_name": "Employee",
                "organization": obj.organization,
            },
        )[0],
    )

    employee_code = factory.Sequence(
        lambda n: f"EMP{n:06d}",
    )

    designation = "Test Engineer"

    hire_date = date(
        2025,
        1,
        1,
    )

    is_active = True


class NoteTemplateFactory(factory.django.DjangoModelFactory):
    """
    Factory for NoteTemplate model.
    """

    class Meta:
        model = NoteTemplate

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    name = factory.Sequence(
        lambda n: f"Template {n}",
    )

    template_type = TemplateType.SOAP

    content = factory.LazyFunction(
        lambda: {
            "sections": [
                "subjective",
                "objective",
                "assessment",
                "plan",
            ],
        },
    )

    is_active = True

    is_system_template = False


class ClinicalNoteFactory(factory.django.DjangoModelFactory):
    """
    Factory for ClinicalNote model.
    """

    class Meta:
        model = ClinicalNote

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    note_type = NoteType.SOAP

    title = factory.Sequence(
        lambda n: f"Clinical Note {n}",
    )

    content = factory.LazyFunction(
        lambda: {
            "subjective": "Patient feels well.",
            "objective": "Vitals are normal.",
            "assessment": "Healthy.",
            "plan": "Continue current treatment.",
        },
    )

    raw_text = ""

    is_amended = False

    amendment_reason = ""

    signed_at = None

    signed_by = None

    created_by = factory.SubFactory(
        EmployeeFactory,
        organization=factory.SelfAttribute(
            "..organization",
        ),
    )


__all__ = [
    "ClinicalNoteFactory",
    "EmployeeFactory",
    "NoteTemplateFactory",
]
