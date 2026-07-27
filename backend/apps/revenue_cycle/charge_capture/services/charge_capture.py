"""
Charge Capture services.
"""

from __future__ import annotations

from apps.revenue_cycle.charge_capture.models import ChargeCapture
from apps.revenue_cycle.components import RcmService

create_charge = None
update_charge = None
delete_charge = None


class ChargeCaptureService(RcmService):
    """
    Write-side operations for charge capture records.
    """

    model = ChargeCapture


create_charge = ChargeCaptureService.create
update_charge = ChargeCaptureService.update
delete_charge = ChargeCaptureService.delete


__all__ = [
    "ChargeCaptureService",
    "create_charge",
    "delete_charge",
    "update_charge",
]
