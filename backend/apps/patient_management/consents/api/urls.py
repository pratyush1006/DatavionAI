"""
Patient Consent API URL entry point.

The detailed consent routes are maintained in the api.urls package.
"""

from __future__ import annotations

from apps.patient_management.consents.api.urls.consent import (
    urlpatterns,
)

__all__ = ("urlpatterns",)
