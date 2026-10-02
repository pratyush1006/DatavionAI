"""
Holiday permission classes.
"""

from .holiday import (
    CanCreateHoliday,
    CanDeleteHoliday,
    CanUpdateHoliday,
    CanViewHoliday,
)

__all__ = [
    "CanViewHoliday",
    "CanCreateHoliday",
    "CanUpdateHoliday",
    "CanDeleteHoliday",
]
