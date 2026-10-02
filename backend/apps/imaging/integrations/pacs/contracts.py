from typing import Protocol


class PACSGateway(Protocol):
    def resolve_study(self, study_instance_uid): ...
