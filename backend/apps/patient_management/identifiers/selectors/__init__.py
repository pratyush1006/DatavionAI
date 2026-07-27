"""
Selectors for the Patient Identifiers module.
"""

from .patient_identifier import (
    get_identifier_by_id,
    get_identifier_by_value,
    get_patient_identifiers,
    get_primary_identifier,
)

__all__ = [
    "get_identifier_by_id",
    "get_identifier_by_value",
    "get_patient_identifiers",
    "get_primary_identifier",
]
