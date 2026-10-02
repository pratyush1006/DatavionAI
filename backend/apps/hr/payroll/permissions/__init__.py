"""
Payroll permission classes.
"""

from .payslip import (
    CanCreatePayslip,
    CanDeletePayslip,
    CanProcessPayslip,
    CanReleasePayslip,
    CanUpdatePayslip,
    CanViewPayslip,
)
from .salary_structure import (
    CanCreateSalaryStructure,
    CanDeleteSalaryStructure,
    CanUpdateSalaryStructure,
    CanViewSalaryStructure,
)

__all__ = [
    "CanViewSalaryStructure",
    "CanCreateSalaryStructure",
    "CanUpdateSalaryStructure",
    "CanDeleteSalaryStructure",
    "CanViewPayslip",
    "CanCreatePayslip",
    "CanUpdatePayslip",
    "CanDeletePayslip",
    "CanProcessPayslip",
    "CanReleasePayslip",
]
