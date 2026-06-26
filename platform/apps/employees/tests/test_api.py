from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class EmployeeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

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

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@datavion.ai",
            password="admin123",
            organization=self.organization,
        )

        self.employee_user = User.objects.create_user(
            username="john",
            password="password123",
            first_name="John",
            last_name="Doe",
            organization=self.organization,
        )

        self.client.force_authenticate(
            user=self.admin,
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            department=self.department,
            team=self.team,
            user=self.employee_user,
            employee_code="EMP001",
            designation="Software Engineer",
            hire_date="2026-06-26",
        )

    def _get_results(self, response):
        """
        Support both paginated and non-paginated responses.
        """
        if isinstance(response.data, dict):
            return response.data.get(
                "results",
                [],
            )

        return response.data

    def test_list_employees(self):
        response = self.client.get("/api/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = self._get_results(response)

        self.assertEqual(
            len(results),
            1,
        )

    def test_employee_detail(self):
        response = self.client.get(
            f"/api/employees/{self.employee.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["employee_code"],
            "EMP001",
        )

    def test_create_employee(self):
        new_user = User.objects.create_user(
            username="alice",
            password="password123",
            organization=self.organization,
        )

        payload = {
            "organization": self.organization.id,
            "department": self.department.id,
            "team": self.team.id,
            "user": new_user.id,
            "employee_code": "EMP002",
            "designation": "QA Engineer",
            "manager": None,
            "hire_date": "2026-06-26",
            "is_active": True,
        }

        response = self.client.post(
            "/api/employees/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_patch_employee(self):
        response = self.client.patch(
            f"/api/employees/{self.employee.id}/",
            {
                "designation": "Senior Software Engineer",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.employee.refresh_from_db()

        self.assertEqual(
            self.employee.designation,
            "Senior Software Engineer",
        )

    def test_delete_employee(self):
        response = self.client.delete(
            f"/api/employees/{self.employee.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Employee.objects.filter(
                pk=self.employee.pk,
            ).exists()
        )

    def test_search_employee(self):
        response = self.client.get(
            "/api/employees/?search=EMP001",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_filter_employee(self):
        response = self.client.get(
            f"/api/employees/?department={self.department.id}",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_order_employee(self):
        response = self.client.get(
            "/api/employees/?ordering=employee_code",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
