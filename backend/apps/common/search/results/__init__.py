"""
DatavionOS Search Results Framework.
"""

from __future__ import annotations

from .normalizer import (
    SearchResultNormalizer,
    search_result_normalizer,
)
from .serializer import (
    SearchResponseSerializer,
)
from .types import (
    SearchItem,
    SearchPagination,
    SearchResponse,
)

__all__: tuple[str, ...] = (
    "SearchItem",
    "SearchPagination",
    "SearchResponse",
    "SearchResultNormalizer",
    "search_result_normalizer",
    "SearchResponseSerializer",
)
