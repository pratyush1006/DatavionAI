"""
Standardized API response helpers.
"""

from __future__ import annotations

from collections.abc import Mapping

from rest_framework import status
from rest_framework.response import Response

from apps.common.exceptions.codes import ErrorCode


def success_response(
    *,
    data: object | None = None,
    message: str = "Success.",
    meta: Mapping[str, object] | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Return a standardized success response.

    Args:
        data: Response payload.
        message: Human-readable success message.
        meta: Optional response metadata (pagination, request_id, etc.).
        status_code: HTTP status code.

    Returns:
        DRF Response with standardized success format.
    """

    payload: dict[str, object] = {
        "success": True,
        "message": message,
        "data": data,
    }

    if meta is not None:
        payload["meta"] = meta

    return Response(
        payload,
        status=status_code,
    )


def created_response(
    *,
    data: object | None = None,
    message: str = "Created successfully.",
    meta: Mapping[str, object] | None = None,
) -> Response:
    """
    Return a standardized HTTP 201 Created response.
    """

    return success_response(
        data=data,
        message=message,
        meta=meta,
        status_code=status.HTTP_201_CREATED,
    )


def error_response(
    *,
    code: ErrorCode = ErrorCode.VALIDATION_ERROR,
    message: str = "Validation failed.",
    details: Mapping[str, object] | None = None,
    meta: Mapping[str, object] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return a standardized error response.

    Args:
        code: Platform error code.
        message: Human-readable error message.
        details: Optional validation or error details.
        meta: Optional response metadata.
        status_code: HTTP status code.

    Returns:
        DRF Response with standardized error format.
    """

    error_payload: dict[str, object] = {
        "code": code.value if hasattr(code, "value") else str(code),
        "message": message,
    }

    if details is not None:
        error_payload["details"] = details

    payload: dict[str, object] = {
        "success": False,
        "error": error_payload,
    }

    if meta is not None:
        payload["meta"] = meta

    return Response(
        payload,
        status=status_code,
    )


def no_content_response() -> Response:
    """
    Return a standardized HTTP 204 No Content response.
    """

    return Response(status=status.HTTP_204_NO_CONTENT)


__all__ = [
    "success_response",
    "created_response",
    "error_response",
    "no_content_response",
]
