"""
Base storage provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorageProvider(ABC):
    """
    Abstract base class for all storage providers.
    """

    @abstractmethod
    def upload(
        self,
        *,
        file: BinaryIO,
        storage_key: str,
        content_type: str,
    ) -> str:
        """
        Upload a file to the storage backend.

        Returns:
            The provider-specific storage path or identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def download(
        self,
        *,
        storage_key: str,
    ) -> BinaryIO:
        """
        Download a file from the storage backend.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete a file from the storage backend.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        *,
        storage_key: str,
    ) -> bool:
        """
        Check whether a file exists.
        """
        raise NotImplementedError

    @abstractmethod
    def url(
        self,
        *,
        storage_key: str,
        expires_in: int | None = None,
    ) -> str:
        """
        Return a URL for accessing the file.

        For private assets, implementations may generate a
        signed URL using ``expires_in``.
        """
        raise NotImplementedError
