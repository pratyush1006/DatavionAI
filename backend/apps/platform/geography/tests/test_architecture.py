"""
Architecture tests for the Geography refresh.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_current_location_layers_exist():
    """Current location is exposed through API -> service -> provider layers."""
    assert (ROOT / "api/geography/views/current_location.py").exists()
    assert (ROOT / "services/current_location.py").exists()
    assert (ROOT / "services/geocoding.py").exists()
    assert (ROOT / "providers/nominatim.py").exists()
    assert (ROOT / "services/reference_resolution.py").exists()


def test_live_tracking_layers_exist():
    """Live tracking has persistence, REST, WebSocket and routing layers."""
    assert (ROOT / "models/tracking.py").exists()
    assert (ROOT / "services/tracking.py").exists()
    assert (ROOT / "consumers.py").exists()
    assert (ROOT / "routing.py").exists()
    assert (ROOT / "migrations/0002_live_tracking.py").exists()
