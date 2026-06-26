from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.employees.services import (
    create_employee,
    delete_employee,
    update_employee,
)
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class EmployeeServiceTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Datavion Analytics",
            code="DAT",
        )

        self.department = Department.objects.create(
            organization=self.organization,
            name="AI Engineering",
            code="AI",
        )

        self.team = Team.objects.create(
            department=self.department,
            name="Backend Team",
            code="BACKEND",
        )

        self.user = User.objects.create_user(
            username="john",
            password="password123",
            first_name="John",
            last_name="Doe",
            organization=self.organization,
        )

    def test_create_employee(self):
        employee = create_employee(
            {
                "organization": self.organization,
                "department": self.department,
                "team": self.team,
                "user": self.user,
                "employee_code": "EMP001",
                "designation": "Software Engineer",
                "manager": None,
                "hire_date": "2026-06-26",
                "is_active": True,
            }
        )

        self.assertEqual(
            employee.employee_code,
            "EMP001",
        )

    def test_update_employee(self):
        employee = create_employee(
            {
                "organization": self.organization,
                "department": self.department,
                "team": self.team,
                "user": self.user,
                "employee_code": "EMP001",
                "designation": "Software Engineer",
                "manager": None,
                "hire_date": "2026-06-26",
                "is_active": True,
            }
        )

        employee = update_employee(
            employee,
            {
                "designation": "Senior Software Engineer",
            },
        )

        self.assertEqual(
            employee.designation,
            "Senior Software Engineer",
        )

    def test_delete_employee(self):
        employee = create_employee(
            {
                "organization": self.organization,
                "department": self.department,
                "team": self.team,
                "user": self.user,
                "employee_code": "EMP001",
                "designation": "Software Engineer",
                "manager": None,
                "hire_date": "2026-06-26",
                "is_active": True,
            }
        )

        delete_employee(employee)

        self.assertFalse(
            Employee.objects.filter(
                pk=employee.pk,
            ).exists()
        )

    def test_invalid_department_for_organization(self):
        other_organization = Organization.objects.create(
            name="Another Org",
            code="ORG2",
        )

        other_department = Department.objects.create(
            organization=other_organization,
            name="Finance",
            code="FIN",
        )

        with self.assertRaises(ValidationError):
            create_employee(
                {
                    "organization": self.organization,
                    "department": other_department,
                    "team": None,
                    "user": self.user,
                    "employee_code": "EMP001",
                    "designation": "Engineer",
                    "manager": None,
                    "hire_date": "2026-06-26",
                    "is_active": True,
                }
            )

    def test_invalid_team_for_department(self):
        other_department = Department.objects.create(
            organization=self.organization,
            name="Finance",
            code="FIN",
        )

        other_team = Team.objects.create(
            department=other_department,
            name="Accounts",
            code="ACC",
        )

        with self.assertRaises(ValidationError):
            create_employee(
                {
                    "organization": self.organization,
                    "department": self.department,
                    "team": other_team,
                    "user": self.user,
                    "employee_code": "EMP001",
                    "designation": "Engineer",
                    "manager": None,
                    "hire_date": "2026-06-26",
                    "is_active": True,
                }
            )

    def test_duplicate_employee_code(self):
        create_employee(
            {
                "organization": self.organization,
                "department": self.department,
                "team": self.team,
                "user": self.user,
                "employee_code": "EMP001",
                "designation": "Engineer",
                "manager": None,
                "hire_date": "2026-06-26",
                "is_active": True,
            }
        )

        second_user = User.objects.create_user(
            username="alice",
            password="password123",
            organization=self.organization,
        )

        with self.assertRaises(ValidationError):
            create_employee(
                {
                    "organization": self.organization,
                    "department": self.department,
                    "team": self.team,
                    "user": second_user,
                    "employee_code": "EMP001",
                    "designation": "Engineer",
                    "manager": None,
                    "hire_date": "2026-06-26",
                    "is_active": True,
                }
            )
