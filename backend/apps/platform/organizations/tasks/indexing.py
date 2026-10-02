"""
Organization indexing tasks.
"""

from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def index_organization(
    *,
    organization_id: UUID,
) -> None:
    """
    Index an organization for search.

    Future search providers:

    - Elasticsearch
    - OpenSearch
    - Meilisearch
    """
    logger.info(
        "Organization indexing started.",
        extra={
            "organization_id": str(organization_id),
        },
    )


def rebuild_organization_index() -> None:
    """
    Rebuild the complete organization search index.
    """
    logger.info(
        "Organization index rebuild started.",
    )


__all__: tuple[str, ...] = (
    "index_organization",
    "rebuild_organization_index",
)
