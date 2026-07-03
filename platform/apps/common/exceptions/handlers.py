"""
Custom DRF exception handler.

This module centralizes exception handling across the Datavion AI
platform while preserving DRF's standard behavior for expected
exceptions and providing consistent responses for unexpected errors.
"""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.common.api.responses import error_response
from apps.common.exceptions.base import DatavionException
from apps.common.exceptions.codes import ErrorCode

logger = logging.getLogger(__name__)


def map_exception_to_error_code(exc: Exception) -> ErrorCode:
    """
    Map DRF exceptions to Datavion API error codes.
    """

    if isinstance(exc, ValidationError):
        return ErrorCode.VALIDATION_ERROR

    if isinstance(exc, NotAuthenticated):
        return ErrorCode.AUTHENTICATION_REQUIRED

    if isinstance(exc, PermissionDenied):
        return ErrorCode.PERMISSION_DENIED

    if isinstance(exc, NotFound):
        return ErrorCode.RESOURCE_NOT_FOUND

    return ErrorCode.INVALID_REQUEST


def custom_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    """
    Handle exceptions consistently across the Datavion platform.

    Datavion domain exceptions are handled first. Any remaining
    Django REST Framework exceptions are delegated to DRF's default
    exception handler and converted into the Datavion response format.
    Unexpected exceptions are logged and returned as HTTP 500.
    """

    # ------------------------------------------------------------------
    # Handle Datavion domain exceptions.
    # ------------------------------------------------------------------
    if isinstance(exc, DatavionException):
        return error_response(
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
            status_code=exc.status_code,
        )

    # ------------------------------------------------------------------
    # Let DRF handle framework exceptions.
    # ------------------------------------------------------------------
    response = exception_handler(
        exc,
        context,
    )

    if response is not None:
        error_code = map_exception_to_error_code(exc)

        if isinstance(exc, ValidationError):
            message = "Validation failed."
            details = response.data
        else:
            message = response.data.get(
                "detail",
                "Request failed.",
            )
            details = None

        return error_response(
            code=error_code,
            message=message,
            details=details,
            status_code=response.status_code,
        )

    # ------------------------------------------------------------------
    # Unexpected exception.
    # ------------------------------------------------------------------
    logger.exception(
        "Unhandled API exception.",
        exc_info=exc,
    )

    message = str(exc) if settings.DEBUG else "An unexpected error occurred."

    return error_response(
        code=ErrorCode.SERVER_ERROR,
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


__all__ = [
    "custom_exception_handler",
]
