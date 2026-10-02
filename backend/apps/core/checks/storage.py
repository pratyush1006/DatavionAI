"""
Storage system checks for the DatavionOS platform.

Validates file storage configuration used by:
- documents
- patient records
- reports
- uploads
- exports
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Warning, register


@register()
@register()
@register()
@register()
def storage_check(*args, **kwargs):

    legacy = getattr(settings, "DEFAULT_FILE_STORAGE", "")
    storages = getattr(settings, "STORAGES", {}) or {}
    default = storages.get("default", {}) if isinstance(storages, dict) else {}
    backend = default.get("BACKEND") if isinstance(default, dict) else ""

    if legacy or backend:
        return []

    return [
        Warning(
            "Default storage backend is not configured.",
            hint="Configure STORAGES['default']['BACKEND'] or DEFAULT_FILE_STORAGE.",
            id="datavion.W002",
        )
    ]


__all__ = [
    "storage_check",
]
