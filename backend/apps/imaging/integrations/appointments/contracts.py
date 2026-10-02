from typing import Protocol


class AppointmentGateway(Protocol):
    def get_appointment(self, appointment_id): ...
