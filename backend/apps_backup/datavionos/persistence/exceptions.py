"""
Persistence exceptions.
"""

from __future__ import annotations


class PersistenceError(Exception):
    """
    Base exception for the persistence subsystem.
    """


class RepositoryError(PersistenceError):
    """
    Raised when repository operations fail.
    """


class TransactionError(PersistenceError):
    """
    Raised when transaction operations fail.
    """


class UnitOfWorkError(PersistenceError):
    """
    Raised when unit of work operations fail.
    """


class StorageProviderError(PersistenceError):
    """
    Raised when storage provider operations fail.
    """


class SpecificationError(PersistenceError):
    """
    Raised when a query specification is invalid.
    """


__all__ = [
    "PersistenceError",
    "RepositoryError",
    "TransactionError",
    "UnitOfWorkError",
    "StorageProviderError",
    "SpecificationError",
]
