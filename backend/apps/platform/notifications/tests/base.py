"""
Base test classes for Notifications.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.accounts.models import User
from apps.platform.notifications.models import Notification


class BaseNotificationTestCase(
    TestCase,
):
    """
    Base test class for notification tests.
    """

    def create_user(
        self,
    ) -> User:
        return User.objects.create_user(
            email="john@example.com",
            password="Password@123",
            first_name="John",
            last_name="Doe",
        )

    def create_notification(
        self,
        *,
        user: User | None = None,
    ) -> Notification:
        return Notification.objects.create(
            user=user,
            recipient="john@example.com",
            recipient_name="John Doe",
            subject="Test Notification",
            template="verification_otp",
            context={
                "otp": "123456",
            },
        )
