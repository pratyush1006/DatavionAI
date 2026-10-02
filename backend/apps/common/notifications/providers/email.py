"""
SMTP email notification provider for DatavionOS.

The provider is responsible only for email transport.

Notification construction and business meaning remain owned by
the application/domain layer.
"""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from apps.common.notifications.models import Notification

from .base import BaseNotificationProvider


class EmailProvider(BaseNotificationProvider):
    """
    Email notification provider.

    Uses Django's configured email backend.

    The provider expects the canonical DatavionOS notification
    contract:

    - recipient.address
    - recipient.name
    - payload
    - template
    - name
    """

    @staticmethod
    def _build_subject(
        notification: Notification,
    ) -> str:
        """
        Resolve the email subject.

        The canonical Notification model intentionally does not
        contain a subject field, so subjects are derived from
        notification identity at the infrastructure boundary.
        """

        subjects: dict[str, str] = {
            "EMAIL_VERIFICATION_OTP": ("DatavionOS Email Verification Code"),
            "LOGIN_OTP": ("DatavionOS Login Verification Code"),
            "LOGIN_ALERT": ("DatavionOS Security Alert"),
        }

        return subjects.get(
            notification.name,
            "DatavionOS Notification",
        )

    @staticmethod
    def _build_context(
        notification: Notification,
    ) -> dict[str, Any]:
        """
        Build email template context from the canonical notification.

        Payload contains notification-specific values while recipient
        information supplies recipient-level template values.
        """

        context = dict(notification.payload)

        context.setdefault(
            "name",
            notification.recipient.name or notification.recipient.address or "",
        )

        context.setdefault(
            "email",
            notification.recipient.address or "",
        )

        context.setdefault(
            "now",
            timezone.now(),
        )

        return context

    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send an email notification.

        Raises:
            ValueError:
                If the notification has no recipient address.

            ValueError:
                If no template is configured.

            Exception:
                If Django's configured email backend fails.
        """

        recipient = notification.recipient.address

        if not recipient:
            raise ValueError(
                "Email notification requires a recipient address.",
            )

        if not notification.template:
            raise ValueError(
                "Email notification requires a template.",
            )

        context = self._build_context(
            notification,
        )

        html_template = f"email/{notification.template}.html"

        text_template = f"email/{notification.template}.txt"

        html_body = render_to_string(
            html_template,
            context,
        )

        try:
            text_body = render_to_string(
                text_template,
                context,
            )
        except Exception:
            text_body = ""

        message = EmailMultiAlternatives(
            subject=self._build_subject(
                notification,
            ),
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        message.attach_alternative(
            html_body,
            "text/html",
        )

        message.send(
            fail_silently=False,
        )

        return True


__all__ = ("EmailProvider",)
