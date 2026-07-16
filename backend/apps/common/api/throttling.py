"""
Reusable API throttling classes.

This module provides a centralized import location for the
throttling classes used across the Datavion AI platform.

Datavion currently uses DRF's default throttling classes.
Custom throttles should only be introduced when a genuine
cross-cutting requirement exists.
"""

from __future__ import annotations

from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)

__all__ = [
    "AnonRateThrottle",
    "ScopedRateThrottle",
    "UserRateThrottle",
]
