"""
Custom DRF exception handler.

This module centralizes exception handling across the Datavion
platform while preserving DRF's standard response format.

Responsibilities
----------------
- Preserve DRF validation errors.
- Preserve authentication and permission responses.
- Log unexpected exceptions.
- Return a generic 500 response in production.
"""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    """
    Handle API exceptions consistently across the platform.

    Expected DRF exceptions are handled using DRF's default
    implementation. Unexpected exceptions are logged and
    converted into a generic server error response.
    """

    response = exception_handler(exc, context)

    if response is not None:
        return response

    logger.exception(
        "Unhandled API exception.",
        exc_info=exc,
    )

    if settings.DEBUG:
        return Response(
            {
                "detail": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {
            "detail": ("An unexpected error occurred."),
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


__all__ = [
    "custom_exception_handler",
]
