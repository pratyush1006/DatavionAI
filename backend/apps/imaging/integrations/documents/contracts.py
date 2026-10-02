from typing import Protocol


class DocumentGateway(Protocol):
    def create_document_link(self, *, study_id, document_id): ...
