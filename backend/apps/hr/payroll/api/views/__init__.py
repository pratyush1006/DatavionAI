"""
Payroll API views.
"""

from .payslip import (
    PayslipListCreateAPIView,
    PayslipRetrieveUpdateDestroyAPIView,
)
from .salary_structure import (
    SalaryStructureListCreateAPIView,
    SalaryStructureRetrieveUpdateDestroyAPIView,
)
from .workflow import (
    PayslipMarkPaidAPIView,
    PayslipProcessAPIView,
)

__all__ = [
    "SalaryStructureListCreateAPIView",
    "SalaryStructureRetrieveUpdateDestroyAPIView",
    "PayslipListCreateAPIView",
    "PayslipRetrieveUpdateDestroyAPIView",
    "PayslipProcessAPIView",
    "PayslipMarkPaidAPIView",
]
