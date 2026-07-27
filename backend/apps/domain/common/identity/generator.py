"""
Identity generator contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.domain.common.identity.entity_id import (
    EntityId,
)


@runtime_checkable
class IdentityGenerator(
    Protocol,
):
    """
    Identity generator.
    """

    def generate(
        self,
    ) -> EntityId: ...
