"""
DatavionOS persistence contracts.
"""

from __future__ import annotations

from .exceptions import (
    PersistenceError,
    RepositoryError,
    SpecificationError,
    StorageProviderError,
    TransactionError,
    UnitOfWorkError,
)
from .repository import (
    Repository,
)
from .services import (
    PersistenceServices,
)
from .specification import (
    Pagination,
    Sort,
    Specification,
    SpecificationEvaluator,
)
from .storage import (
    StorageProvider,
)
from .transaction import (
    Transaction,
    TransactionStatus,
)
from .unit_of_work import (
    UnitOfWork,
)

__all__ = [
    # Repository
    "Repository",
    # Specification
    "Specification",
    "SpecificationEvaluator",
    "Sort",
    "Pagination",
    # Transaction
    "Transaction",
    "TransactionStatus",
    # Unit of Work
    "UnitOfWork",
    # Storage
    "StorageProvider",
    # Service aggregation
    "PersistenceServices",
    # Exceptions
    "PersistenceError",
    "RepositoryError",
    "SpecificationError",
    "StorageProviderError",
    "TransactionError",
    "UnitOfWorkError",
]
