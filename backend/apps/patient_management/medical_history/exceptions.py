"""Domain exceptions for Patient Medical History."""

from __future__ import annotations

from apps.common.exceptions import DatavionException
from apps.common.exceptions.codes import ErrorCode


class MedicalHistoryError(DatavionException):
    """MedicalHistoryError implementation."""

    default_code = ErrorCode.VALIDATION_ERROR
    default_detail = "Medical history operation failed."


class MedicalHistoryNotFoundError(MedicalHistoryError):
    """MedicalHistoryNotFoundError implementation."""

    default_code = ErrorCode.NOT_FOUND
    default_detail = "Medical history was not found."


class MedicalHistoryPermissionError(MedicalHistoryError):
    """MedicalHistoryPermissionError implementation."""

    default_code = ErrorCode.PERMISSION_DENIED
    default_detail = "You do not have permission for this medical-history operation."


__all__ = (
    "MedicalHistoryError",
    "MedicalHistoryNotFoundError",
    "MedicalHistoryPermissionError",
)
