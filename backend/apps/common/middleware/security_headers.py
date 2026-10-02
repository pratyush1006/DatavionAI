"""
Security headers middleware.

Adds standard HTTP security headers to every response.

Content-Security-Policy (CSP) is intentionally omitted because it
depends on frontend and deployment configuration.
"""

from __future__ import annotations

from typing import Final

from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)

X_CONTENT_TYPE_OPTIONS = "X-Content-Type-Options"

X_FRAME_OPTIONS = "X-Frame-Options"

REFERRER_POLICY = "Referrer-Policy"

PERMISSIONS_POLICY = "Permissions-Policy"

CROSS_ORIGIN_OPENER_POLICY = "Cross-Origin-Opener-Policy"

CROSS_ORIGIN_RESOURCE_POLICY = "Cross-Origin-Resource-Policy"

STRICT_TRANSPORT_SECURITY = "Strict-Transport-Security"


SECURITY_HEADERS: Final[dict[str, str]] = {
    X_CONTENT_TYPE_OPTIONS: "nosniff",
    X_FRAME_OPTIONS: "DENY",
    REFERRER_POLICY: ("strict-origin-when-cross-origin"),
    PERMISSIONS_POLICY: (
        "accelerometer=(), "
        "camera=(), "
        "geolocation=(), "
        "gyroscope=(), "
        "microphone=(), "
        "payment=(), "
        "usb=()"
    ),
    CROSS_ORIGIN_OPENER_POLICY: ("same-origin"),
    CROSS_ORIGIN_RESOURCE_POLICY: ("same-origin"),
}


HSTS_VALUE = "max-age=31536000; includeSubDomains"


class SecurityHeadersMiddleware(
    BaseMiddleware,
):
    """
    Apply security headers to responses.
    """

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Add security headers.
        """

        for header, value in SECURITY_HEADERS.items():
            response.setdefault(
                header,
                value,
            )

        enable_hsts = getattr(
            settings,
            "SECURITY_ENABLE_HSTS",
            False,
        )

        if enable_hsts:
            response.setdefault(
                STRICT_TRANSPORT_SECURITY,
                HSTS_VALUE,
            )

        return response


__all__: tuple[str, ...] = ("SecurityHeadersMiddleware",)
