"""
Request ID storage.

Stores the current request ID in thread-local storage so it
can be accessed from anywhere during request processing.
"""

from threading import local

_storage = local()


def set_request_id(request_id: str) -> None:
    _storage.request_id = request_id


def get_request_id() -> str | None:
    return getattr(_storage, "request_id", None)


def clear_request_id() -> None:
    if hasattr(_storage, "request_id"):
        del _storage.request_id
