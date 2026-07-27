"""
Security system checks for the DatavionOS platform.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Error, Warning, register


@register()
def security_check(
    app_configs,
    **kwargs,
):
    """
    Validate critical security settings.
    """

    messages = []

    # ------------------------------------------------------------------
    # Secret key
    # ------------------------------------------------------------------

    if not settings.SECRET_KEY:
        messages.append(
            Error(
                "SECRET_KEY is not configured.",
                hint="Configure SECRET_KEY using environment variables.",
                id="datavion.E003",
            )
        )

    # ------------------------------------------------------------------
    # Timezone
    # ------------------------------------------------------------------

    if not settings.USE_TZ:
        messages.append(
            Warning(
                "USE_TZ should be enabled.",
                hint="Enable timezone aware datetime handling.",
                id="datavion.W001",
            )
        )

    # ------------------------------------------------------------------
    # Debug mode
    # ------------------------------------------------------------------

    if getattr(settings, "DEBUG", False):
        messages.append(
            Warning(
                "DEBUG mode is enabled.",
                hint="Disable DEBUG in production environments.",
                id="datavion.W007",
            )
        )

    # ------------------------------------------------------------------
    # Allowed hosts
    # ------------------------------------------------------------------

    allowed_hosts = getattr(
        settings,
        "ALLOWED_HOSTS",
        [],
    )

    if not allowed_hosts:
        messages.append(
            Warning(
                "ALLOWED_HOSTS is empty.",
                hint="Configure trusted application domains.",
                id="datavion.W008",
            )
        )

    # ------------------------------------------------------------------
    # Secure cookies
    # ------------------------------------------------------------------

    if not getattr(
        settings,
        "SESSION_COOKIE_SECURE",
        False,
    ):
        messages.append(
            Warning(
                "SESSION_COOKIE_SECURE is disabled.",
                hint="Enable secure cookies in production.",
                id="datavion.W009",
            )
        )

    if not getattr(
        settings,
        "CSRF_COOKIE_SECURE",
        False,
    ):
        messages.append(
            Warning(
                "CSRF_COOKIE_SECURE is disabled.",
                hint="Enable secure CSRF cookies in production.",
                id="datavion.W010",
            )
        )

    return messages
