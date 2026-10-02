"""
Workflow for one-time current-location resolution.
"""

from __future__ import annotations

from apps.platform.geography.services.current_location import CurrentLocationService


def resolve_current_location(
    *,
    latitude,
    longitude,
    accuracy_meters: float | None = None,
) -> dict:
    """Resolve current coordinates exactly once."""
    return CurrentLocationService().resolve(
        latitude=latitude,
        longitude=longitude,
        accuracy_meters=accuracy_meters,
    )


__all__ = ("resolve_current_location",)
