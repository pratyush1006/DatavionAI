"""
Department permission exports.
"""

from .department import (
    CanCreateDepartment,
    CanDeleteDepartment,
    CanUpdateDepartment,
    CanViewDepartment,
)

__all__ = [
    "CanCreateDepartment",
    "CanDeleteDepartment",
    "CanUpdateDepartment",
    "CanViewDepartment",
]
