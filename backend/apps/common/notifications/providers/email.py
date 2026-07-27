"""
SMTP email provider.
"""

from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.common.notifications.providers.base import (
    BaseNotificationProvider,
)
from apps.platform.notifications.models import Notification


class EmailProvider(
    BaseNotificationProvider,
):
    """
    SMTP email provider.
    """

    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send an email notification.
        """

        html_body = render_to_string(
            f"email/{notification.template}.html",
            notification.context,
        )

        try:
            text_body = render_to_string(
                f"email/{notification.template}.txt",
                notification.context,
            )
        except Exception:
            text_body = ""

        message = EmailMultiAlternatives(
            subject=notification.subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                notification.recipient,
            ],
        )

        message.attach_alternative(
            html_body,
            "text/html",
        )

        message.send(
            fail_silently=False,
        )

        #
        # Save provider metadata.
        #
        notification.provider_response = {
            "backend": settings.EMAIL_BACKEND,
            "recipient": notification.recipient,
            "subject": notification.subject,
        }

        #
        # Django SMTP backend does not expose
        # a provider message id.
        #
        notification.provider_message_id = ""

        notification.save(
            update_fields=[
                "provider_response",
                "provider_message_id",
                "updated_at",
            ],
        )

        return True


__all__ = [
    "EmailProvider",
]
