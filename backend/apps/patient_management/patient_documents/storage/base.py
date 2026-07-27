"""
Abstract storage provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import BinaryIO

from apps.patient_management.patient_documents.storage.types import (
    StorageObject,
)


class StorageProvider(ABC):
    """
    Enterprise storage provider interface.
    """

    @abstractmethod
    def upload(
        self,
        *,
        path: str,
        file: BinaryIO,
        content_type: str,
    ) -> StorageObject:
        """
        Upload a file.
        """

    @abstractmethod
    def download(
        self,
        *,
        path: str,
    ) -> BinaryIO:
        """
        Download a file.
        """

    @abstractmethod
    def delete(
        self,
        *,
        path: str,
    ) -> None:
        """
        Delete a file.
        """

    @abstractmethod
    def exists(
        self,
        *,
        path: str,
    ) -> bool:
        """
        Check whether the object exists.
        """

    @abstractmethod
    def metadata(
        self,
        *,
        path: str,
    ) -> StorageObject:
        """
        Return object metadata.
        """

    @abstractmethod
    def generate_signed_url(
        self,
        *,
        path: str,
        expires_in: int = 300,
    ) -> str:
        """
        Generate a signed URL.
        """

    @abstractmethod
    def copy(
        self,
        *,
        source: str,
        destination: str,
    ) -> StorageObject:
        """
        Copy an object.
        """

    @abstractmethod
    def move(
        self,
        *,
        source: str,
        destination: str,
    ) -> StorageObject:
        """
        Move an object.
        """


__all__ = [
    "StorageProvider",
]
