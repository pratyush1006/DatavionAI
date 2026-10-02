"""
Document management constants.

Defines controlled vocabularies for the
DatavionOS Document Management bounded context.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

# ============================================================
# Document Status
# ============================================================


class DocumentStatus(
    models.TextChoices,
):
    """
    Document lifecycle status.
    """

    DRAFT = (
        "draft",
        _("Draft"),
    )

    ACTIVE = (
        "active",
        _("Active"),
    )

    ARCHIVED = (
        "archived",
        _("Archived"),
    )

    DELETED = (
        "deleted",
        _("Deleted"),
    )


DEFAULT_DOCUMENT_STATUS = DocumentStatus.ACTIVE


# ============================================================
# Document Type
# ============================================================


class DocumentType(
    models.TextChoices,
):
    """
    Supported document categories.
    """

    GENERAL = (
        "general",
        _("General Document"),
    )

    CONTRACT = (
        "contract",
        _("Contract"),
    )

    IDENTIFICATION = (
        "identification",
        _("Identification Document"),
    )

    MEDICAL_RECORD = (
        "medical_record",
        _("Medical Record"),
    )

    REPORT = (
        "report",
        _("Report"),
    )

    PRESCRIPTION = (
        "prescription",
        _("Prescription"),
    )

    CONSENT = (
        "consent",
        _("Consent Document"),
    )

    INSURANCE = (
        "insurance",
        _("Insurance Document"),
    )

    INVOICE = (
        "invoice",
        _("Invoice"),
    )


DEFAULT_DOCUMENT_TYPE = DocumentType.GENERAL


# ============================================================
# Document Access Level
# ============================================================


class DocumentAccessLevel(
    models.TextChoices,
):
    """
    Document visibility levels.
    """

    PRIVATE = (
        "private",
        _("Private"),
    )

    ORGANIZATION = (
        "organization",
        _("Organization"),
    )

    TENANT = (
        "tenant",
        _("Tenant"),
    )

    PUBLIC = (
        "public",
        _("Public"),
    )


DEFAULT_ACCESS_LEVEL = DocumentAccessLevel.PRIVATE


# ============================================================
# Version Status
# ============================================================


class DocumentVersionStatus(
    models.TextChoices,
):
    """
    Document version lifecycle.
    """

    CURRENT = (
        "current",
        _("Current"),
    )

    SUPERSEDED = (
        "superseded",
        _("Superseded"),
    )

    ARCHIVED = (
        "archived",
        _("Archived"),
    )


# ============================================================
# Access Permission
# ============================================================


class DocumentPermission(
    models.TextChoices,
):
    """
    Document access permissions.
    """

    VIEW = (
        "view",
        _("View"),
    )

    DOWNLOAD = (
        "download",
        _("Download"),
    )

    EDIT = (
        "edit",
        _("Edit"),
    )

    SHARE = (
        "share",
        _("Share"),
    )

    DELETE = (
        "delete",
        _("Delete"),
    )


__all__ = (
    "DocumentStatus",
    "DEFAULT_DOCUMENT_STATUS",
    "DocumentType",
    "DEFAULT_DOCUMENT_TYPE",
    "DocumentAccessLevel",
    "DEFAULT_ACCESS_LEVEL",
    "DocumentVersionStatus",
    "DocumentPermission",
)
