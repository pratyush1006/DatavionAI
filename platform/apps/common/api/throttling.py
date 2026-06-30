"""
Reusable API throttling classes.

Datavion currently uses the default DRF throttling classes.
Custom throttles should only be added when required.
"""

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
