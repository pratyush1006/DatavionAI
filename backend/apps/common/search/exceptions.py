"""
DatavionOS Search Exceptions.
"""

from __future__ import annotations


class SearchError(Exception):
    """
    Base search exception.
    """


class SearchProviderError(SearchError):
    """
    Provider execution failure.
    """


class SearchProviderNotFoundError(SearchError):
    """
    Provider unavailable.
    """


__all__ = (
    "SearchError",
    "SearchProviderError",
    "SearchProviderNotFoundError",
)
