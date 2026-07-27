"""
Clock abstraction.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(
    Protocol,
):
    """
    Clock abstraction.
    """

    def now(
        self,
    ) -> datetime:
        """
        Return the current UTC time.
        """
