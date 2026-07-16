"""
Diagnosis permission exports.
"""

from .diagnosis import (
    CanCreateDiagnosis,
    CanDeleteDiagnosis,
    CanUpdateDiagnosis,
    CanViewDiagnosis,
)

__all__ = [
    "CanCreateDiagnosis",
    "CanDeleteDiagnosis",
    "CanUpdateDiagnosis",
    "CanViewDiagnosis",
]
