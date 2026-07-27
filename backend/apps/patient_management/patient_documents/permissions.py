"""
Permissions for the Patient Documents module.
"""

from __future__ import annotations


class PatientDocumentPermission:
    """
    Permission codes for the Patient Documents module.
    """

    MODULE = "patient_documents"

    VIEW = f"{MODULE}.view"
    LIST = f"{MODULE}.list"
    CREATE = f"{MODULE}.create"
    UPDATE = f"{MODULE}.update"
    DELETE = f"{MODULE}.delete"

    UPLOAD = f"{MODULE}.upload"
    DOWNLOAD = f"{MODULE}.download"

    ARCHIVE = f"{MODULE}.archive"
    RESTORE = f"{MODULE}.restore"

    SHARE = f"{MODULE}.share"
    EXPORT = f"{MODULE}.export"
    IMPORT = f"{MODULE}.import"

    AUDIT = f"{MODULE}.audit"

    ALL = (
        VIEW,
        LIST,
        CREATE,
        UPDATE,
        DELETE,
        UPLOAD,
        DOWNLOAD,
        ARCHIVE,
        RESTORE,
        SHARE,
        EXPORT,
        IMPORT,
        AUDIT,
    )


__all__ = [
    "PatientDocumentPermission",
]
