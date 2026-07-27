"""
HTTP status utilities.

Provides reusable HTTP status helpers for the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import TypeAlias

Status: TypeAlias = HTTPStatus

StatusCode: TypeAlias = int | HTTPStatus


def _value(
    status_code: StatusCode,
) -> int:
    """
    Return the integer value of a status code.
    """

    if isinstance(
        status_code,
        HTTPStatus,
    ):
        return status_code.value

    return status_code


def is_informational(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code is informational.
    """

    code = _value(
        status_code,
    )

    return 100 <= code < 200


def is_success(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code indicates success.
    """

    code = _value(
        status_code,
    )

    return 200 <= code < 300


def is_redirect(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code indicates a redirect.
    """

    code = _value(
        status_code,
    )

    return 300 <= code < 400


def is_client_error(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code indicates a client error.
    """

    code = _value(
        status_code,
    )

    return 400 <= code < 500


def is_server_error(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code indicates a server error.
    """

    code = _value(
        status_code,
    )

    return 500 <= code < 600


def is_error(
    status_code: StatusCode,
) -> bool:
    """
    Return whether the status code indicates an error.
    """

    return (
        _value(
            status_code,
        )
        >= 400
    )


__all__: tuple[str, ...] = (
    "Status",
    "StatusCode",
    "is_client_error",
    "is_error",
    "is_informational",
    "is_redirect",
    "is_server_error",
    "is_success",
)
