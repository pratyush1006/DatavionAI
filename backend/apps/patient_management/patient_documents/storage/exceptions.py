"""
Storage exceptions.
"""

from __future__ import annotations


class StorageError(Exception):
    """
    Base storage exception.
    """


class FileNotFound(StorageError):
    """
    File does not exist.
    """


class UploadFailed(StorageError):
    """
    Upload failed.
    """


class DownloadFailed(StorageError):
    """
    Download failed.
    """


class DeleteFailed(StorageError):
    """
    Delete failed.
    """


__all__ = [
    "StorageError",
    "FileNotFound",
    "UploadFailed",
    "DownloadFailed",
    "DeleteFailed",
]
