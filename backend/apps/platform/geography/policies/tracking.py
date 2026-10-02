"""Policies for validating device tracking samples."""

from __future__ import annotations

MAX_ACCURACY_METERS = 10000.0
MAX_SPEED_MPS = 100.0


def validate_tracking_sample(
    *, accuracy_meters=None, speed_mps=None, heading_degrees=None
):
    if accuracy_meters is not None and not 0 <= accuracy_meters <= MAX_ACCURACY_METERS:
        raise ValueError("accuracy_meters is outside the supported range.")
    if speed_mps is not None and not 0 <= speed_mps <= MAX_SPEED_MPS:
        raise ValueError("speed_mps is outside the supported range.")
    if heading_degrees is not None and not 0 <= heading_degrees <= 360:
        raise ValueError("heading_degrees must be between 0 and 360.")


__all__ = ("MAX_ACCURACY_METERS", "MAX_SPEED_MPS", "validate_tracking_sample")
