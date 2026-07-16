"""
Request ID middleware.
"""

from __future__ import annotations

import uuid

from django.utils.deprecation import MiddlewareMixin

from .request_id import (
    clear_request_id,
    set_request_id,
)


class RequestIDMiddleware(
    MiddlewareMixin,
):
    """
    Middleware that assigns a request ID to every request.
    """

    def process_request(
        self,
        request,
    ) -> None:
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid.uuid4()),
        )

        request.request_id = request_id

        set_request_id(
            request_id,
        )

    def process_response(
        self,
        request,
        response,
    ):
        request_id = getattr(
            request,
            "request_id",
            None,
        )

        if request_id:
            response["X-Request-ID"] = request_id

        clear_request_id()

        return response
