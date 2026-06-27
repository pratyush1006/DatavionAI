from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.departments.models import Department
from apps.organizations.models import Organization
from apps.teams.models import Team

User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test case shared across all test modules.
    """

    def setUp(self):
        super().setUp()

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


class BaseAPITestCase(BaseTestCase):
    """
    Base API test case with authenticated client.
    """

    def setUp(self):
        super().setUp()

        self.client = APIClient()

        self.client.force_authenticate(
            user=self.admin,
        )
