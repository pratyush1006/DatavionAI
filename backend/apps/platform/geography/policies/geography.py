"""
Policies for current-location resolution.
"""

from __future__ import annotations


def validate_accuracy(accuracy_meters: float | None) -> None:
    """Validate optional browser-reported accuracy."""
    if accuracy_meters is not None and accuracy_meters < 0:
        raise ValueError("accuracy_meters cannot be negative.")


__all__ = ("validate_accuracy",)
