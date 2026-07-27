"""
DatavionOS Search Result Serializer.

Converts search objects into API payloads.
"""

from __future__ import annotations

from dataclasses import asdict

from .types import (
    SearchResponse,
)


class SearchResponseSerializer:
    """
    Serialize SearchResponse.
    """

    @staticmethod
    def serialize(
        response: SearchResponse,
    ) -> dict:
        """
        Convert response into dictionary.
        """

        return asdict(
            response,
        )


__all__: tuple[str, ...] = ("SearchResponseSerializer",)
