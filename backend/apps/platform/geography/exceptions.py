"""
Domain exceptions for platform Geography.
"""

from __future__ import annotations


class GeographyError(Exception):
    """Base Geography exception."""


class InvalidCoordinatesError(GeographyError):
    """Raised when coordinates are outside valid Earth bounds."""


class GeocodingProviderError(GeographyError):
    """Raised when an external geocoding provider fails."""


__all__ = ("GeographyError", "InvalidCoordinatesError", "GeocodingProviderError")
