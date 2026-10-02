"""
Request ID middleware.

Provides unique request identification for the DatavionAI
request lifecycle.

Request IDs are used for:

- distributed tracing
- structured logging
- audit correlation
- API debugging
"""

from __future__ import annotations

from uuid import (
    UUID,
    uuid4,
)

from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)
from apps.common.middleware.context import (
    get_request_id,
    set_request_id,
)

REQUEST_ID_HEADER = "X-Request-ID"

MAX_REQUEST_ID_LENGTH = 64


def _is_valid_request_id(
    value: str,
) -> bool:
    """
    Validate incoming request ID.
    """

    if not value:
        return False

    if len(value) > MAX_REQUEST_ID_LENGTH:
        return False

    try:
        UUID(value)

    except ValueError:
        return False

    return True


class RequestIDMiddleware(
    BaseMiddleware,
):
    """
    Assign a unique request ID to every request.

    Incoming request IDs are reused only when valid.
    """

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Create or reuse request ID.
        """

        incoming_id = request.headers.get(
            REQUEST_ID_HEADER,
        )

        request_id = (
            incoming_id
            if incoming_id
            and _is_valid_request_id(
                incoming_id,
            )
            else str(
                uuid4(),
            )
        )

        request.request_id = request_id

        set_request_id(
            request_id,
        )

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Add request ID response header.
        """

        request_id = get_request_id()

        if request_id:
            response[REQUEST_ID_HEADER] = request_id

        return response


__all__: tuple[str, ...] = (
    "REQUEST_ID_HEADER",
    "RequestIDMiddleware",
)
