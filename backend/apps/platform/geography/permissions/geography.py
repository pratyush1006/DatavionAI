"""
Permissions for Geography endpoints.
"""

from __future__ import annotations

from rest_framework.permissions import AllowAny


class GeographyCurrentLocationPermission(AllowAny):
    """Allow coordinate resolution; clients must explicitly obtain device permission."""


__all__ = ("GeographyCurrentLocationPermission",)
