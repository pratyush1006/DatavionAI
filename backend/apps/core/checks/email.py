"""
Email system checks for the DatavionOS platform.

Validates email delivery configuration.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Tags, Warning, register


@register(Tags.compatibility)
def email_check(
    app_configs,
    **kwargs,
):
    """
    Validate email backend configuration.
    """

    messages = []

    backend = getattr(
        settings,
        "EMAIL_BACKEND",
        "",
    )

    if not backend:
        messages.append(
            Warning(
                "EMAIL_BACKEND is not configured.",
                hint=("Configure email backend before enabling email features."),
                id="datavion.W004",
            )
        )

        return messages

    # SMTP configuration validation

    if "smtp" in backend.lower():
        email_host = getattr(
            settings,
            "EMAIL_HOST",
            "",
        )

        if not email_host:
            messages.append(
                Warning(
                    "EMAIL_HOST is not configured.",
                    hint=("Configure SMTP server details for email delivery."),
                    id="datavion.W012",
                )
            )

    # Sender validation

    default_sender = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        "",
    )

    if not default_sender:
        messages.append(
            Warning(
                "DEFAULT_FROM_EMAIL is not configured.",
                hint=("Configure default sender email for system notifications."),
                id="datavion.W013",
            )
        )

    return messages


__all__ = [
    "email_check",
]
