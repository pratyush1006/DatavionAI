"""
Leave permission classes.
"""

from .leave_balance import (
    CanCreateLeaveBalance,
    CanDeleteLeaveBalance,
    CanUpdateLeaveBalance,
    CanViewLeaveBalance,
)
from .leave_request import (
    CanApproveLeaveRequest,
    CanCreateLeaveRequest,
    CanDeleteLeaveRequest,
    CanUpdateLeaveRequest,
    CanViewLeaveRequest,
)
from .leave_type import (
    CanCreateLeaveType,
    CanDeleteLeaveType,
    CanUpdateLeaveType,
    CanViewLeaveType,
)

__all__ = [
    "CanViewLeaveType",
    "CanCreateLeaveType",
    "CanUpdateLeaveType",
    "CanDeleteLeaveType",
    "CanViewLeaveBalance",
    "CanCreateLeaveBalance",
    "CanUpdateLeaveBalance",
    "CanDeleteLeaveBalance",
    "CanViewLeaveRequest",
    "CanCreateLeaveRequest",
    "CanUpdateLeaveRequest",
    "CanDeleteLeaveRequest",
    "CanApproveLeaveRequest",
]
