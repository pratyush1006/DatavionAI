"""
Standardized API response helpers for the DatavionOS platform.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Final, TypeAlias

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.exceptions.codes import ErrorCode

SUCCESS_MESSAGE: Final[str] = "Success."
CREATED_MESSAGE: Final[str] = "Created successfully."
VALIDATION_ERROR_MESSAGE: Final[str] = "Validation failed."

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]

JSONDict: TypeAlias = dict[str, JSONValue]
Headers: TypeAlias = Mapping[str, str]
Meta: TypeAlias = Mapping[str, JSONValue]


def _timestamp() -> str:
    """
    Return the current UTC timestamp in ISO-8601 format.
    """

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _request_metadata(
    request: Request | None = None,
) -> JSONDict:
    """
    Build common response metadata.
    """

    metadata: JSONDict = {
        "api_version": getattr(settings, "API_VERSION", "v1"),
        "timestamp": _timestamp(),
    }

    if request is None:
        return metadata

    if request_id := getattr(request, "request_id", None):
        metadata["request_id"] = str(request_id)

    tenant = getattr(request, "tenant", None)

    if tenant is not None:
        tenant_id = getattr(tenant, "id", None)

        if tenant_id is not None:
            metadata["tenant_id"] = str(tenant_id)

    return metadata


def _build_response(
    *,
    payload: Mapping[str, JSONValue] | None = None,
    status_code: int,
    headers: Headers | None = None,
) -> Response:
    """
    Build a standardized HTTP response.
    """

    return Response(
        data=payload,
        status=status_code,
        headers=headers,
    )


def success_response(
    *,
    data: JSONValue = None,
    message: str = SUCCESS_MESSAGE,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Return a successful response.
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
    data: JSONValue = None,
    message: str = CREATED_MESSAGE,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
) -> Response:
    """
    Return an HTTP 201 response.
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
    details: JSONValue = None,
    meta: Meta | None = None,
    headers: Headers | None = None,
    request: Request | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return a standardized error response.
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
    Return an HTTP 204 response.
    """

    return _build_response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers=headers,
    )


__all__ = (
    "JSONDict",
    "JSONPrimitive",
    "JSONValue",
    "Headers",
    "Meta",
    "created_response",
    "error_response",
    "no_content_response",
    "success_response",
)
