"""
Standardized API response helpers for the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Final, TypeAlias

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.exceptions.codes import ErrorCode

SUCCESS_MESSAGE: Final[str] = "Success."

CREATED_MESSAGE: Final[str] = "Created successfully."

VALIDATION_ERROR_MESSAGE: Final[str] = "Validation failed."


JSONDict: TypeAlias = dict[str, Any]

Headers: TypeAlias = Mapping[str, str]

Meta: TypeAlias = Mapping[str, Any]


def _timestamp() -> str:
    """
    Return UTC timestamp.
    """

    return (
        datetime.now(UTC)
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    )


def _request_metadata(
    request: Request | None = None,
) -> JSONDict:
    """
    Build common response metadata.
    """

    metadata: JSONDict = {
        "api_version": getattr(
            settings,
            "API_VERSION",
            "v1",
        ),
        "timestamp": _timestamp(),
    }

    if request is not None:
        request_id = getattr(
            request,
            "request_id",
            None,
        )

        if request_id:
            metadata["request_id"] = str(
                request_id,
            )

        tenant = getattr(
            request,
            "tenant",
            None,
        )

        if tenant:
            metadata["tenant_id"] = str(
                tenant.id,
            )

    return metadata


def _build_response(
    *,
    payload: Mapping[str, Any] | None = None,
    status_code: int,
    headers: Headers | None = None,
) -> Response:
    """
    Build standardized HTTP response.
    """

    return Response(
        data=payload,
        status=status_code,
        headers=headers,
    )


def success_response(
    *,
    data: Any = None,
    message: str = SUCCESS_MESSAGE,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Return successful response.
    """

    payload: JSONDict = {
        "success": True,
        "message": message,
        "data": data,
        "meta": {
            **_request_metadata(request),
            **dict(meta or {}),
        },
    }

    return _build_response(
        payload=payload,
        status_code=status_code,
        headers=headers,
    )


def created_response(
    *,
    data: Any = None,
    message: str = CREATED_MESSAGE,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
) -> Response:
    """
    Return HTTP 201 response.
    """

    return success_response(
        data=data,
        message=message,
        meta=meta,
        headers=headers,
        request=request,
        status_code=status.HTTP_201_CREATED,
    )


def error_response(
    *,
    code: ErrorCode = ErrorCode.VALIDATION_ERROR,
    message: str = VALIDATION_ERROR_MESSAGE,
    details: Any = None,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return standardized error response.
    """

    payload: JSONDict = {
        "success": False,
        "error": {
            "code": code.value,
            "message": message,
            "details": details,
        },
        "meta": {
            **_request_metadata(request),
            **dict(meta or {}),
        },
    }

    return _build_response(
        payload=payload,
        status_code=status_code,
        headers=headers,
    )


def no_content_response(
    *,
    headers: Headers | None = None,
) -> Response:
    """
    Return HTTP 204 response.
    """

    return _build_response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers=headers,
    )


__all__: tuple[str, ...] = (
    "created_response",
    "error_response",
    "no_content_response",
    "success_response",
)
