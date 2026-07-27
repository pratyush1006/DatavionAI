"""
DatavionAI Exception Utilities.

Reusable helper functions for working with DatavionAI exceptions.

Design Principles
-----------------
- Framework agnostic
- Stateless
- Pure functions
- Serialization friendly
"""

from __future__ import annotations

from traceback import format_exception
from typing import Any

from .base import DatavionException

###############################################################################
# Serialization
###############################################################################


def exception_to_dict(
    exception: DatavionException,
) -> dict[str, Any]:
    """
    Serialize a DatavionException into a dictionary.
    """

    return exception.to_dict()


###############################################################################
# Root Cause
###############################################################################


def get_root_exception(
    exception: BaseException,
) -> BaseException:
    """
    Return the root exception in an exception chain.
    """

    current = exception

    while current.__cause__ is not None:
        current = current.__cause__

    return current


###############################################################################
# Traceback
###############################################################################


def format_traceback(
    exception: BaseException,
) -> str:
    """
    Return a formatted traceback string.
    """

    return "".join(
        format_exception(
            type(exception),
            exception,
            exception.__traceback__,
        )
    )


###############################################################################
# Type Checking
###############################################################################


def is_datavion_exception(
    exception: BaseException,
) -> bool:
    """
    Return True if the exception is a DatavionException.
    """

    return isinstance(
        exception,
        DatavionException,
    )


###############################################################################
# Safe Message
###############################################################################


def get_safe_message(
    exception: BaseException,
) -> str:
    """
    Return a user-safe exception message.
    """

    if isinstance(
        exception,
        DatavionException,
    ):
        return exception.message

    return "An unexpected error occurred."


###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "exception_to_dict",
    "format_traceback",
    "get_root_exception",
    "get_safe_message",
    "is_datavion_exception",
)
