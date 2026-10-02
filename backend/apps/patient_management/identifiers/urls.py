"""Legacy compatibility URLConf for Patient Management identifiers.

Canonical ownership:
    config.urls
        -> apps.patient_management.urls
        -> apps.patient_management.api.urls
        -> apps.patient_management.identifiers.api.urls

This module intentionally contains no URL registrations.

It is retained only so legacy imports continue to resolve without
registering the canonical API routes a second time.

# DATAVIONOS_LEGACY_URLCONF_COMPATIBILITY_STUB
"""

from django.urls import URLPattern, URLResolver

app_name = "identifiers-legacy"

urlpatterns: list[URLPattern | URLResolver] = []
