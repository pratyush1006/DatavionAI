"""
Immutable event payload for one-time current-location resolution.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrentLocationResolved:
    """Describe a completed current-location resolution."""

    latitude: float
    longitude: float
    provider: str


__all__ = ("CurrentLocationResolved",)
