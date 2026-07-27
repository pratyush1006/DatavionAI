"""
Organization import tasks.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def import_organizations(
    *,
    file_path: str | Path,
) -> None:
    """
    Import organizations from an external file.

    Supported formats (future):

    - CSV
    - Excel
    - JSON
    """
    logger.info(
        "Organization import started.",
        extra={
            "file_path": str(file_path),
        },
    )


def validate_import_file(
    *,
    file_path: str | Path,
) -> None:
    """
    Validate an organization import file.
    """
    logger.info(
        "Organization import validation started.",
        extra={
            "file_path": str(file_path),
        },
    )


__all__: tuple[str, ...] = (
    "import_organizations",
    "validate_import_file",
)
