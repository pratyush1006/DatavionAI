from collections.abc import Mapping

from rest_framework import status
from rest_framework.response import Response


def success_response(
    *,
    data: object | None = None,
    message: str = "Success.",
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Return a standardized successful API response.

    Example:
    {
        "success": true,
        "message": "Employee retrieved successfully.",
        "data": {...}
    }
    """

    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def created_response(
    *,
    data: object | None = None,
    message: str = "Created successfully.",
) -> Response:
    """
    Return a standardized HTTP 201 Created response.
    """

    return success_response(
        data=data,
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


def error_response(
    *,
    errors: Mapping[str, object] | None = None,
    message: str = "Validation failed.",
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Return a standardized error response.

    Example:
    {
        "success": false,
        "message": "Validation failed.",
        "errors": {
            "employee_code": [
                "This field must be unique."
            ]
        }
    }
    """

    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )


def no_content_response() -> Response:
    """
    Return a standardized HTTP 204 No Content response.
    """

    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )
