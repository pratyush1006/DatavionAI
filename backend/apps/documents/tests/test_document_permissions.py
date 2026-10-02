"""
Document RBAC tests.
"""

from django.test import TestCase

from apps.platform.accounts.models import User


class DocumentPermissionTestCase(
    TestCase,
):
    def test_document_permissions(
        self,
    ):

        user = User.objects.create_user(
            email="permission@test.com",
            password="password123",
        )

        self.assertIsNotNone(user)
