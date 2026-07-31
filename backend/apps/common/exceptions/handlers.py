"""
DatavionAI exception handler.

Centralized exception handler for Django REST Framework.

Design Principles
-----------------
- Consistent API responses
- Framework integration
- Enterprise logging
- Secure error handling
- Stable error contract
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from http import HTTPStatus
from typing import Final

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .base import (
    DatavionException,
)
from .codes import (
    ErrorCode,
)
from .messages import (
    get_error_message,
)

logger = logging.getLogger(__name__)


# ============================================================
# HTTP -> ErrorCode mapping
# ============================================================


_STATUS_CODE_MAP: Final[dict[int, ErrorCode]] = {
    status.HTTP_400_BAD_REQUEST: (ErrorCode.BAD_REQUEST),
    status.HTTP_401_UNAUTHORIZED: (ErrorCode.UNAUTHENTICATED),
    status.HTTP_403_FORBIDDEN: (ErrorCode.FORBIDDEN),
    status.HTTP_404_NOT_FOUND: (ErrorCode.RESOURCE_NOT_FOUND),
    status.HTTP_405_METHOD_NOT_ALLOWED: (ErrorCode.OPERATION_NOT_ALLOWED),
    status.HTTP_409_CONFLICT: (ErrorCode.RESOURCE_CONFLICT),
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: (ErrorCode.UNSUPPORTED_MEDIA_TYPE),
    status.HTTP_429_TOO_MANY_REQUESTS: (ErrorCode.RATE_LIMIT_EXCEEDED),
}


# ============================================================
# Metadata
# ============================================================


def _meta(
    request: object | None,
) -> dict[str, str]:
    """
    Build common response metadata.
    """

    meta: dict[str, str] = {
        "timestamp": timezone.now().isoformat(),
        "api_version": getattr(
            settings,
            "API_VERSION",
            "v1",
        ),
    }

    if request is None:
        return meta

    if request_id := getattr(
        request,
        "request_id",
        None,
    ):
        meta["request_id"] = str(
            request_id,
        )

    tenant = getattr(
        request,
        "tenant",
        None,
    )

    if tenant is not None:
        tenant_id = getattr(
            tenant,
            "id",
            None,
        )

        if tenant_id is not None:
            meta["tenant_id"] = str(
                tenant_id,
            )

    return meta


# ============================================================
# Payload
# ============================================================


def _payload(
    *,
    code: ErrorCode,
    message: str,
    detail: object,
    meta: Mapping[str, object],
) -> dict[str, object]:
    """
    Build standardized error payload.
    """

    return {
        "success": False,
        "status": "error",
        "error": {
            "code": code.value,
            "message": message,
            "details": detail,
        },
        "meta": dict(meta),
    }


# ============================================================
# DRF Exception Handler
# ============================================================


def datavion_exception_handler(
    exc: Exception,
    context: dict[str, object],
) -> Response:
    """
    Enterprise DRF exception handler.
    """

    response = exception_handler(
        exc,
        context,
    )

    request = context.get(
        "request",
    )

    #
    # Datavion custom exceptions
    #
    if isinstance(
        exc,
        DatavionException,
    ):
        payload = _payload(
            code=exc.code,
            message=exc.message,
            detail=exc.detail,
            meta=_meta(request),
        )

        if exc.extra:
            payload["meta"]["extra"] = exc.extra

        return Response(
            payload,
            status=exc.status_code,
        )

    #
    # DRF handled exceptions
    #
    if response is not None:
        status_code = response.status_code

        code = _STATUS_CODE_MAP.get(
            status_code,
            ErrorCode.BAD_REQUEST,
        )

        response.data = _payload(
            code=code,
            message=get_error_message(
                code,
            ),
            detail=response.data,
            meta=_meta(request),
        )

        return response

    #
    # Unexpected exceptions
    #
    logger.exception(
        "Unhandled exception",
        exc_info=exc,
    )

    detail: object = None

    if settings.DEBUG:
        detail = str(
            exc,
        )

    return Response(
        _payload(
            code=(ErrorCode.INTERNAL_SERVER_ERROR),
            message=get_error_message(
                ErrorCode.INTERNAL_SERVER_ERROR,
            ),
            detail=detail,
            meta=_meta(request),
        ),
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


__all__ = ("datavion_exception_handler",)
