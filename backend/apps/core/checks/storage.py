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
from django.core.checks import Error, Warning, register


@register()
def storage_check(
    app_configs,
    **kwargs,
):
    """
    Validate storage configuration.
    """

    messages = []

    storage_backend = getattr(
        settings,
        "DEFAULT_FILE_STORAGE",
        "",
    )

    if not storage_backend:
        messages.append(
            Warning(
                "DEFAULT_FILE_STORAGE is not configured.",
                hint=("Configure local, S3, Azure or another storage backend."),
                id="datavion.W002",
            )
        )

    media_root = getattr(
        settings,
        "MEDIA_ROOT",
        "",
    )

    if not media_root and not storage_backend:
        messages.append(
            Error(
                "No storage location is configured.",
                hint=("Configure MEDIA_ROOT or a cloud storage backend."),
                id="datavion.E006",
            )
        )

    # ------------------------------------------------------------------
    # S3 validation
    # ------------------------------------------------------------------

    if "s3" in storage_backend.lower() and not getattr(
        settings,
        "AWS_ACCESS_KEY_ID",
        None,
    ):
        messages.append(
            Warning(
                "AWS_ACCESS_KEY_ID is not configured.",
                hint="Configure AWS credentials for S3 storage.",
                id="datavion.W014",
            )
        )

    # ------------------------------------------------------------------
    # Azure validation
    # ------------------------------------------------------------------

    if "azure" in storage_backend.lower() and not getattr(
        settings,
        "AZURE_ACCOUNT_NAME",
        None,
    ):
        messages.append(
            Warning(
                "AZURE_ACCOUNT_NAME is not configured.",
                hint="Configure Azure Blob Storage settings.",
                id="datavion.W015",
            )
        )

    return messages


__all__ = [
    "storage_check",
]
