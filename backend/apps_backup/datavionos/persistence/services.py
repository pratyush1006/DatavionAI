"""
Persistence service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.persistence.storage import (
    StorageProvider,
)
from apps.datavionos.persistence.unit_of_work import (
    UnitOfWork,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PersistenceServices:
    """
    Aggregate of persistence services.
    """

    storage: StorageProvider

    unit_of_work: UnitOfWork


__all__ = [
    "PersistenceServices",
]
