"""
Services for the Patient Preferences module.
"""

from .communication_preference import (
    create_communication_preference,
    delete_communication_preference,
    update_communication_preference,
)
from .preference import (
    create_patient_preference,
    delete_patient_preference,
    update_patient_preference,
)

__all__ = [
    "create_communication_preference",
    "create_patient_preference",
    "delete_communication_preference",
    "delete_patient_preference",
    "update_communication_preference",
    "update_patient_preference",
]
