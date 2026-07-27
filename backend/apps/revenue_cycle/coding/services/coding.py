"""
Coding Entry services.
"""

from __future__ import annotations

from apps.revenue_cycle.coding.models import ChargeCoding
from apps.revenue_cycle.components import RcmService

create_coding = None
update_coding = None
delete_coding = None


class ChargeCodingService(RcmService):
    """
    Write-side operations for coding entry records.
    """

    model = ChargeCoding


create_coding = ChargeCodingService.create
update_coding = ChargeCodingService.update
delete_coding = ChargeCodingService.delete


__all__ = [
    "ChargeCodingService",
    "create_coding",
    "delete_coding",
    "update_coding",
]
