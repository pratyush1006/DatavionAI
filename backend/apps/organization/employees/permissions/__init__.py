"""
Employee permission classes.
"""

from .employee import (
    CanCreateEmployee,
    CanDeleteEmployee,
    CanUpdateEmployee,
    CanViewEmployee,
)

__all__ = [
    "CanViewEmployee",
    "CanCreateEmployee",
    "CanUpdateEmployee",
    "CanDeleteEmployee",
]
