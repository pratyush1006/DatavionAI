"""
Employee services.

Central export point for employee
business operations.
"""

from __future__ import annotations

from .assignment import (
    change_employee_assignment,
)
from .contract import (
    create_employee_contract,
    update_employee_contract,
)
from .employee import (
    create_employee,
    delete_employee,
    update_employee,
)

__all__ = [
    "create_employee",
    "update_employee",
    "delete_employee",
    "change_employee_assignment",
    "create_employee_contract",
    "update_employee_contract",
]
