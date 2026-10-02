"""Legacy compatibility URLConf for Patient Management family_members.

Canonical ownership:
    config.urls
        -> apps.patient_management.urls
        -> apps.patient_management.api.urls
        -> apps.patient_management.family_members.api.urls

This module intentionally contains no URL registrations.

It is retained only so legacy imports continue to resolve without
registering the canonical API routes a second time.

# DATAVIONOS_LEGACY_URLCONF_COMPATIBILITY_STUB
"""

from django.urls import URLPattern, URLResolver

app_name = "family_members-legacy"

urlpatterns: list[URLPattern | URLResolver] = []
