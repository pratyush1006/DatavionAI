"""
Shared base test cases.

These classes provide reusable test setup for feature
applications.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.departments.models import Department
from apps.organizations.models import Organization
from apps.teams.models.team import Team

User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test case shared across feature applications.
    """

    def setUp(self) -> None:
        super().setUp()

        self.organization = self.create_organization()

        self.admin = self.create_user(
            username="admin",
            email="admin@datavion.ai",
            password="TestPassword@123",
            organization=self.organization,
            is_superuser=True,
            is_staff=True,
        )

    def create_organization(self, **kwargs) -> Organization:
        """
        Create a test organization.
        """

        defaults = {
            "name": "Datavion Analytics",
            "code": "DAT",
        }
        defaults.update(kwargs)

        return Organization.objects.create(**defaults)

    def create_user(self, **kwargs):
        """
        Create a test user.
        """

        password = kwargs.pop("password", "TestPassword@123")
        is_superuser = kwargs.pop("is_superuser", False)

        if is_superuser:
            return User.objects.create_superuser(
                password=password,
                **kwargs,
            )

        return User.objects.create_user(
            password=password,
            **kwargs,
        )

    def create_department(self, **kwargs) -> Department:
        """
        Create a test department.
        """

        defaults = {
            "organization": self.organization,
            "name": "AI Engineering",
            "code": "AI",
        }
        defaults.update(kwargs)

        return Department.objects.create(**defaults)

    def create_team(self, **kwargs) -> Team:
        """
        Create a test team.
        """

        department = kwargs.pop(
            "department",
            self.create_department(),
        )

        defaults = {
            "department": department,
            "name": "Backend Team",
            "code": "BACKEND",
        }
        defaults.update(kwargs)

        return Team.objects.create(**defaults)


class BaseAPITestCase(BaseTestCase):
    """
    Base API test case with an authenticated client.
    """

    def setUp(self) -> None:
        super().setUp()

        self.client: APIClient = APIClient()

        self.client.force_authenticate(
            user=self.admin,
        )
