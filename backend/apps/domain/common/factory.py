"""
Domain factory contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    TypeVar,
    runtime_checkable,
)

TAggregate = TypeVar("TAggregate")


@runtime_checkable
class Factory[TAggregate](
    Protocol,
):
    """
    Domain factory contract.
    """

    def create(
        self,
        *args: object,
        **kwargs: object,
    ) -> TAggregate:
        """
        Create a new aggregate in a valid state.
        """
