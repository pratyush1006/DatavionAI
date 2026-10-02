from typing import Protocol


class ChargeCaptureGateway(Protocol):
    def create_charge_link(self, *, study_id, charge_id): ...
