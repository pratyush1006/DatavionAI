"""
Standardized API response helpers.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from rest_framework import status
from rest_framework.response import Response

from apps.common.exceptions.codes import ErrorCode

SUCCESS_MESSAGE: Final = "Success."
CREATED_MESSAGE: Final = "Created successfully."
VALIDATION_ERROR_MESSAGE: Final = "Validation failed."

JSONDict = dict[str, object]


def success_response(
    *,
    data: object | None = None,
    message: str = SUCCESS_MESSAGE,
    meta: Mapping[str, object] | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Return a standardized success response.
    """

    payload: JSONDict = {
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
    message: str = CREATED_MESSAGE,
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
    message: str = VALIDATION_ERROR_MESSAGE,
    details: Mapping[str, object] | None = None,
    meta: Mapping[str, object] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return a standardized error response.
    """

    error_payload: JSONDict = {
        "code": code.value,
        "message": message,
    }

    if details is not None:
        error_payload["details"] = details

    payload: JSONDict = {
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

    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )


__all__ = [
    "success_response",
    "created_response",
    "error_response",
    "no_content_response",
]
