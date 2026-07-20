from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class EmployeeAPITestCase(TestCase):
    """
    Test cases for employee API endpoints.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()

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

        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
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

    def test_list_employees(self):
        """
        Test listing employees.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    def test_create_employee(self):
        """
        Test creating an employee.
        """
        self.client.force_authenticate(user=self.admin_user)

        user2 = User.objects.create_user(
            username="newemployee",
            email="new@example.com",
            first_name="New",
            last_name="Employee",
        )

        data = {
            "organization": self.organization.id,
            "department": self.department.id,
            "team": self.team.id,
            "user": user2.id,
            "employee_code": "EMP002",
            "designation": "Developer",
            "hire_date": "2023-06-01",
            "is_active": True,
        }

        response = self.client.post(
            "/api/employees/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["employee_code"], "EMP002")

    def test_retrieve_employee(self):
        """
        Test retrieving a specific employee.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f"/api/employees/{self.employee.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["employee_code"], "EMP001")

    def test_update_employee(self):
        """
        Test updating an employee.
        """
        self.client.force_authenticate(user=self.admin_user)

        data = {
            "designation": "Senior Developer",
        }

        response = self.client.patch(
            f"/api/employees/{self.employee.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["designation"], "Senior Developer")

    def test_delete_employee(self):
        """
        Test deleting an employee.
        """
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(f"/api/employees/{self.employee.id}/")

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=self.employee.id)
