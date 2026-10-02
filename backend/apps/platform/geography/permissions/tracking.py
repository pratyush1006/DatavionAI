"""Permissions for Geography live tracking."""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated


class GeographyTrackingPermission(IsAuthenticated):
    """Require authenticated access to tracking sessions."""


__all__ = ("GeographyTrackingPermission",)
