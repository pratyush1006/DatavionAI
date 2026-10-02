"""
Notification test factories.
"""

from __future__ import annotations

from apps.platform.accounts.models import User
from apps.platform.notifications.models import Notification


def create_test_user() -> User:
    return User.objects.create_user(
        email="john@example.com",
        password="Password@123",
    )


def create_notification(
    *,
    user: User | None = None,
) -> Notification:
    return Notification.objects.create(
        user=user,
        recipient="john@example.com",
        recipient_name="John Doe",
        subject="Test",
        template="verification_otp",
        context={
            "otp": "123456",
        },
    )
