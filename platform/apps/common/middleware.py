import uuid

from .request_id import (
    clear_request_id,
    set_request_id,
)


class RequestIDMiddleware:
    """
    Assigns a unique Request ID to every HTTP request.
    """

    HEADER_NAME = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())

        request.request_id = request_id

        set_request_id(request_id)

        response = self.get_response(request)

        response[self.HEADER_NAME] = request_id

        clear_request_id()

        return response
