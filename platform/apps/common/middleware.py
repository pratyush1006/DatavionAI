"""
Request ID middleware.

Assigns a unique request ID to every incoming HTTP request.
"""

from __future__ import annotations

from collections.abc import Callable
import uuid

from django.http import (
    HttpRequest,
    HttpResponse,
)

from .request_id import (
    clear_request_id,
    set_request_id,
)


class RequestIDMiddleware:
    """
    Assign a unique request ID to every request.
    """

    HEADER_NAME = "X-Request-ID"

    def __init__(
        self,
        get_response: Callable[
            [HttpRequest],
            HttpResponse,
        ],
    ) -> None:
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        request_id = str(uuid.uuid4())

        request.request_id = request_id

        set_request_id(request_id)

        try:
            response = self.get_response(request)
            response[self.HEADER_NAME] = request_id
            return response

        finally:
            clear_request_id()


__all__ = [
    "RequestIDMiddleware",
]
