from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class EmployeeModelTestCase(TestCase):
    """
    Test cases for the Employee model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

        self.department = Department.objects.create(
            name="Test Department",
            organization=self.organization,
        )

        self.team = Team.objects.create(
            name="Test Team",
            department=self.department,
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2023-01-01",
        )

    def test_employee_creation(self):
        """
        Test that an employee is created successfully.
        """
        self.assertEqual(self.employee.employee_code, "EMP001")
        self.assertEqual(self.employee.designation, "Software Engineer")
        self.assertEqual(self.employee.organization, self.organization)
        self.assertEqual(self.employee.department, self.department)
        self.assertEqual(self.employee.team, self.team)
        self.assertEqual(self.employee.user, self.user)
        self.assertTrue(self.employee.is_active)

    def test_employee_full_name(self):
        """
        Test that the full_name property returns the user's full name.
        """
        self.assertEqual(self.employee.full_name, "Test User")

    def test_employee_str(self):
        """
        Test the string representation of an employee.
        """
        expected_str = "EMP001 - Test User"
        self.assertEqual(str(self.employee), expected_str)

    def test_employee_code_uniqueness_per_organization(self):
        """
        Test that employee codes are unique per organization.
        """
        user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            first_name="Test2",
            last_name="User2",
        )

        org2 = Organization.objects.create(
            name="Another Organization",
        )

        dept2 = Department.objects.create(
            name="Another Department",
            organization=org2,
        )

        employee2 = Employee.objects.create(
            organization=org2,
            department=dept2,
            user=user2,
            employee_code="EMP001",
            designation="Manager",
            hire_date="2023-02-01",
        )

        self.assertEqual(employee2.employee_code, "EMP001")
        self.assertNotEqual(employee2.organization, self.employee.organization)

    def test_employee_manager_relationship(self):
        """
        Test the manager relationship.
        """
        user3 = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            first_name="Manager",
            last_name="User",
        )

        manager = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            user=user3,
            employee_code="MGR001",
            designation="Team Lead",
            hire_date="2022-01-01",
        )

        self.employee.manager = manager
        self.employee.save()

        self.employee.refresh_from_db()
        self.assertEqual(self.employee.manager, manager)
        self.assertIn(self.employee, manager.subordinates.all())
