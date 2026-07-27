"""
Selectors for the Patient Relationships module.
"""

from .relationship import (
    get_patient_relationships,
    get_primary_relationship,
    get_relationship_by_id,
    get_relationships_by_type,
)

__all__ = [
    "get_patient_relationships",
    "get_primary_relationship",
    "get_relationship_by_id",
    "get_relationships_by_type",
]
