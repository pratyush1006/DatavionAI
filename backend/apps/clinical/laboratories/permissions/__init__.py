"""
Permission classes for the Laboratories application.
"""

from .laboratory_order import IsLaboratoryOrderUser
from .laboratory_result import IsLaboratoryResultUser
from .laboratory_test import IsLaboratoryTestUser

__all__ = [
    "IsLaboratoryOrderUser",
    "IsLaboratoryResultUser",
    "IsLaboratoryTestUser",
]
