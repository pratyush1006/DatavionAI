"""
Telemedicine serializer exports.
"""

from __future__ import annotations

from .session import (
    DETAIL_FIELDS,
    LIST_FIELDS,
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
    WRITE_FIELDS,
    TelemedicineSessionBaseSerializer,
    TelemedicineSessionCreateSerializer,
    TelemedicineSessionDetailSerializer,
    TelemedicineSessionListSerializer,
    TelemedicineSessionSerializer,
    TelemedicineSessionUpdateSerializer,
)

__all__ = [
    "DETAIL_FIELDS",
    "LIST_FIELDS",
    "READ_ONLY_FIELDS",
    "UPDATE_FIELDS",
    "WRITE_FIELDS",
    "TelemedicineSessionBaseSerializer",
    "TelemedicineSessionCreateSerializer",
    "TelemedicineSessionDetailSerializer",
    "TelemedicineSessionListSerializer",
    "TelemedicineSessionSerializer",
    "TelemedicineSessionUpdateSerializer",
]
