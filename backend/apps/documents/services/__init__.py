"""Document service exports."""

from .access import (
    check_document_access,
    create_document_access,
    revoke_document_access,
)
from .document import (
    archive_document,
    create_document,
    delete_document,
    update_document,
)
from .version import create_document_version

__all__ = (
    "archive_document",
    "check_document_access",
    "create_document",
    "create_document_access",
    "create_document_version",
    "delete_document",
    "revoke_document_access",
    "update_document",
)
