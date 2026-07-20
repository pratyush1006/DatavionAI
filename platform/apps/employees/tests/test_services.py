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


class EmployeeServiceTestCase(TestCase):
    """
    Test cases for employee services.
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

    def test_create_employee(self):
        """
        Test creating an employee through the service.
        """
        validated_data = {
            "organization": self.organization,
            "department": self.department,
            "team": self.team,
            "user": self.user,
            "employee_code": "EMP001",
            "designation": "Software Engineer",
            "hire_date": "2023-01-01",
        }

        employee = create_employee(validated_data=validated_data)

        self.assertEqual(employee.employee_code, "EMP001")
        self.assertEqual(employee.organization, self.organization)
        self.assertTrue(employee.is_active)

    def test_create_employee_validation_error_duplicate_code(self):
        """
        Test that creating an employee with duplicate code raises validation error.
        """
        validated_data = {
            "organization": self.organization,
            "department": self.department,
            "team": self.team,
            "user": self.user,
            "employee_code": "EMP001",
            "designation": "Software Engineer",
            "hire_date": "2023-01-01",
        }

        create_employee(validated_data=validated_data)

        user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
        )

        validated_data["user"] = user2
        with self.assertRaises(ValidationError):
            create_employee(validated_data=validated_data)

    def test_update_employee(self):
        """
        Test updating an employee through the service.
        """
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2023-01-01",
        )

        validated_data = {
            "designation": "Senior Software Engineer",
        }

        updated_employee = update_employee(
            instance=employee,
            validated_data=validated_data,
        )

        self.assertEqual(updated_employee.designation, "Senior Software Engineer")
        self.assertEqual(updated_employee.employee_code, "EMP001")

    def test_delete_employee(self):
        """
        Test deleting an employee through the service.
        """
        employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            user=self.user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2023-01-01",
        )

        employee_id = employee.id

        delete_employee(instance=employee)

        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=employee_id)
