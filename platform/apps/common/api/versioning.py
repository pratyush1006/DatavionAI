"""
Reusable API versioning classes.

Datavion currently uses the default DRF versioning strategies.
Custom versioning implementations should only be added when
required by the platform.
"""

from rest_framework.versioning import (
    NamespaceVersioning,
    URLPathVersioning,
)

__all__ = [
    "NamespaceVersioning",
    "URLPathVersioning",
]
