"""
Request ID storage.

Stores the current request ID in thread-local storage so it
can be accessed from anywhere during request processing.
"""

from __future__ import annotations

from threading import local

_storage: local = local()


def set_request_id(
    request_id: str,
) -> None:
    """
    Store the current request ID.
    """
    _storage.request_id = request_id


def get_request_id() -> str | None:
    """
    Return the current request ID.
    """
    return getattr(
        _storage,
        "request_id",
        None,
    )


def clear_request_id() -> None:
    """
    Remove the current request ID.
    """
    if hasattr(
        _storage,
        "request_id",
    ):
        del _storage.request_id


__all__ = [
    "clear_request_id",
    "get_request_id",
    "set_request_id",
]
