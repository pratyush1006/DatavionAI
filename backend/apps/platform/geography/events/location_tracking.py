"""Event payload for a persisted tracking update."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LocationUpdated:
    session_id: str
    sequence: int
    latitude: float
    longitude: float
    recorded_at: str


__all__ = ("LocationUpdated",)
