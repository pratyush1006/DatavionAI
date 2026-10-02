"""
DatavionOS Search Result Normalizer.

Converts provider-specific results into
a unified SearchResponse.
"""

from __future__ import annotations

from typing import Any

from .types import (
    SearchItem,
    SearchPagination,
    SearchResponse,
)


class SearchResultNormalizer:
    """
    Normalize all search providers.
    """

    def normalize(
        self,
        *,
        items: list[Any],
        provider: str,
        mode: str,
        metadata: dict[str, Any] | None = None,
    ) -> SearchResponse:
        """
        Build standard search response.
        """

        normalized = [
            SearchItem(
                id=str(
                    getattr(
                        item,
                        "id",
                        index,
                    )
                ),
                score=float(
                    getattr(
                        item,
                        "score",
                        0,
                    )
                ),
                content=getattr(
                    item,
                    "content",
                    None,
                ),
                metadata=getattr(
                    item,
                    "metadata",
                    {},
                ),
            )
            for index, item in enumerate(items)
        ]

        return SearchResponse(
            items=normalized,
            total=len(normalized),
            pagination=SearchPagination(
                total=len(normalized),
                total_pages=(1 if normalized else 0),
            ),
            provider=provider,
            mode=mode,
            metadata=metadata or {},
        )


search_result_normalizer = SearchResultNormalizer()


__all__: tuple[str, ...] = (
    "SearchResultNormalizer",
    "search_result_normalizer",
)
