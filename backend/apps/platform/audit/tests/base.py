"""
Base test case for the Audit application.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.platform.organizations.models import Organization

User = get_user_model()


class AuditBaseTestCase(
    TestCase,
):
    """
    Base class shared by all Audit tests.
    """

    @classmethod
    def setUpTestData(
        cls,
    ) -> None:
        """
        Create reusable test data.
        """

        cls.organization = Organization.objects.create(
            name="Datavion Test Organization",
        )

        cls.user = User.objects.create_user(
            username="audituser",
            email="audit@datavion.ai",
            password="TestPassword123!",
        )


__all__ = [
    "AuditBaseTestCase",
]
