"""
Custom DRF exception handler.

This module centralizes exception handling across the Datavion AI
platform while preserving DRF's standard behavior for expected
exceptions and providing consistent responses for unexpected errors.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.common.api.responses import error_response
from apps.common.exceptions.base import DatavionException
from apps.common.exceptions.codes import ErrorCode

logger = logging.getLogger(__name__)

VALIDATION_ERROR_MESSAGE = "Validation failed."
REQUEST_FAILED_MESSAGE = "Request failed."
UNEXPECTED_ERROR_MESSAGE = "An unexpected error occurred."


def map_exception_to_error_code(
    exc: Exception,
) -> ErrorCode:
    """
    Map DRF exceptions to Datavion API error codes.
    """

    if isinstance(
        exc,
        ValidationError,
    ):
        return ErrorCode.VALIDATION_ERROR

    if isinstance(
        exc,
        (
            AuthenticationFailed,
            NotAuthenticated,
        ),
    ):
        return ErrorCode.AUTHENTICATION_REQUIRED

    if isinstance(
        exc,
        PermissionDenied,
    ):
        return ErrorCode.PERMISSION_DENIED

    if isinstance(
        exc,
        NotFound,
    ):
        return ErrorCode.RESOURCE_NOT_FOUND

    if isinstance(
        exc,
        Throttled,
    ):
        return ErrorCode.RATE_LIMIT_EXCEEDED

    if isinstance(
        exc,
        ParseError,
    ):
        return ErrorCode.INVALID_REQUEST

    return ErrorCode.INVALID_REQUEST


def custom_exception_handler(
    exc: Exception,
    context: Mapping[str, Any],
) -> Response | None:
    """
    Handle exceptions consistently across the Datavion AI platform.

    Datavion exceptions are handled first. Remaining Django REST
    Framework exceptions are delegated to DRF's default exception
    handler and converted into the Datavion response format.
    Unexpected exceptions are logged and returned as HTTP 500.
    """

    #
    # Handle Datavion framework/domain exceptions.
    #
    if isinstance(
        exc,
        DatavionException,
    ):
        return error_response(
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
            status_code=exc.status_code,
        )

    #
    # Delegate DRF exceptions.
    #
    response = exception_handler(
        exc,
        context,
    )

    if response is not None:
        error_code = map_exception_to_error_code(
            exc,
        )

        if isinstance(
            exc,
            ValidationError,
        ):
            message = VALIDATION_ERROR_MESSAGE
            details = {
                "errors": response.data,
            }

        elif isinstance(
            response.data,
            dict,
        ):
            message = response.data.get(
                "detail",
                REQUEST_FAILED_MESSAGE,
            )
            details = None

        elif isinstance(
            response.data,
            str,
        ):
            message = response.data
            details = None

        else:
            message = REQUEST_FAILED_MESSAGE
            details = None

        return error_response(
            code=error_code,
            message=message,
            details=details,
            status_code=response.status_code,
        )

    #
    # Unexpected exception.
    #
    request = context.get(
        "request",
    )

    logger.exception(
        "Unhandled API exception.",
        extra={
            "path": (
                request.path
                if isinstance(
                    request,
                    Request,
                )
                else None
            ),
            "method": (
                request.method
                if isinstance(
                    request,
                    Request,
                )
                else None
            ),
            "user": (
                getattr(
                    request.user,
                    "id",
                    None,
                )
                if isinstance(
                    request,
                    Request,
                )
                and hasattr(
                    request,
                    "user",
                )
                else None
            ),
        },
    )

    message = (
        str(
            exc,
        )
        if settings.DEBUG
        else UNEXPECTED_ERROR_MESSAGE
    )

    return error_response(
        code=ErrorCode.SERVER_ERROR,
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


__all__ = [
    "custom_exception_handler",
]
