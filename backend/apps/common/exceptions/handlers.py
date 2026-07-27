"""
DatavionAI Exception Handler.

Centralized exception handler for Django REST Framework.

Design Principles
-----------------
- Consistent API responses
- Framework integration
- Enterprise logging ready
- Safe error messages
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .base import DatavionException
from .codes import ErrorCode
from .messages import get_error_message


def datavion_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response:
    """
    Enterprise DRF exception handler.
    """

    response = exception_handler(
        exc,
        context,
    )

    request = context.get("request")

    request_id = getattr(request, "request_id", None) if request is not None else None

    # ------------------------------------------------------------------
    # Datavion Exceptions
    # ------------------------------------------------------------------

    if isinstance(exc, DatavionException):
        payload = {
            "success": False,
            "status": "error",
            "code": exc.code.value,
            "message": exc.message,
            "detail": exc.detail,
            "meta": {
                "timestamp": timezone.now().isoformat(),
                "request_id": request_id,
            },
        }

        if exc.extra:
            payload["meta"]["extra"] = exc.extra

        return Response(
            payload,
            status=exc.status_code,
        )

    # ------------------------------------------------------------------
    # DRF Exceptions
    # ------------------------------------------------------------------

    if response is not None:
        payload = {
            "success": False,
            "status": "error",
            "code": ErrorCode.BAD_REQUEST.value,
            "message": get_error_message(
                ErrorCode.BAD_REQUEST,
            ),
            "detail": response.data,
            "meta": {
                "timestamp": timezone.now().isoformat(),
                "request_id": request_id,
            },
        }

        response.data = payload
        return response

    # ------------------------------------------------------------------
    # Unhandled Exceptions
    # ------------------------------------------------------------------

    payload = {
        "success": False,
        "status": "error",
        "code": ErrorCode.INTERNAL_SERVER_ERROR.value,
        "message": get_error_message(
            ErrorCode.INTERNAL_SERVER_ERROR,
        ),
        "detail": None,
        "meta": {
            "timestamp": timezone.now().isoformat(),
            "request_id": request_id,
        },
    }

    return Response(
        payload,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


__all__ = ("datavion_exception_handler",)
