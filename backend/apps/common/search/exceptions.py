"""
DatavionOS Search Exceptions.
"""

from __future__ import annotations

from rest_framework.exceptions import APIException


class SearchError(Exception):
    """
    Base search exception.
    """


class SearchProviderError(SearchError):
    """
    Provider execution failure.
    """


class SearchProviderNotFoundError(APIException):
    """Raised when no working search backend is enabled for this deployment."""

    status_code = 503
    default_code = "search_provider_unavailable"
    default_detail = "Search is unavailable because no backend is configured."


__all__ = (
    "SearchError",
    "SearchProviderError",
    "SearchProviderNotFoundError",
)
