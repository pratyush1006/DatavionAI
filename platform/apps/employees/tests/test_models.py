from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class EmployeeModelTest(TestCase):
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
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

        self.assertEqual(
            employee.employee_code,
            "EMP001",
        )

        self.assertTrue(employee.is_active)

    def test_employee_string_representation(self):
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

        self.assertEqual(
            str(employee),
            "EMP001 - John Doe",
        )

    def test_team_can_be_null(self):
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

        self.assertIsNone(employee.team)

    def test_manager_can_be_null(self):
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

        self.assertIsNone(employee.manager)

    def test_unique_employee_code_per_organization(self):
        Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

        second_user = User.objects.create_user(
            username="alice",
            password="password123",
            first_name="Alice",
            last_name="Smith",
            organization=self.organization,
        )

        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                organization=self.organization,
                department=self.department,
                team=self.team,
                user=second_user,
                employee_code="EMP001",
                designation="QA Engineer",
                hire_date="2026-06-26",
            )

    def test_manager_relationship(self):
        manager_user = User.objects.create_user(
            username="manager",
            password="password123",
            first_name="Jane",
            last_name="Manager",
            organization=self.organization,
        )

        manager = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=manager_user,
            employee_code="EMP100",
            designation="Manager",
            hire_date="2026-06-26",
        )

        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP101",
            designation="Developer",
            manager=manager,
            hire_date="2026-06-26",
        )

        self.assertEqual(
            employee.manager,
            manager,
        )

    def test_team_set_null_on_delete(self):
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Developer",
            hire_date="2026-06-26",
        )

        self.team.delete()

        employee.refresh_from_db()

        self.assertIsNone(employee.team)

    def test_manager_set_null_on_delete(self):
        manager_user = User.objects.create_user(
            username="manager",
            password="password123",
            first_name="Jane",
            last_name="Manager",
            organization=self.organization,
        )

        manager = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=manager_user,
            employee_code="EMP100",
            designation="Manager",
            hire_date="2026-06-26",
        )

        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP101",
            designation="Developer",
            manager=manager,
            hire_date="2026-06-26",
        )

        manager.delete()

        employee.refresh_from_db()

        self.assertIsNone(employee.manager)
