"""Explicit contracts for all related Datavion domains."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class IntegrationContext:
    organization_id: str
    patient_id: str
    encounter_id: str | None = None
    correlation_id: str | None = None


class DevicePlatformContract(Protocol):
    def authorize_capture(
        self, *, organization_id: str, device_id: str, patient_id: str
    ) -> dict[str, Any]: ...


class ClinicalNotesContract(Protocol):
    def create_draft(
        self,
        *,
        context: IntegrationContext,
        note_type: str,
        text: str,
        structured_content: dict[str, Any],
    ) -> str: ...


class TelemedicineContract(Protocol):
    def validate_session(
        self, *, organization_id: str, session_id: str, patient_id: str
    ) -> dict[str, Any]: ...
    def attach_transcription(
        self, *, organization_id: str, session_id: str, transcription_session_id: str
    ) -> None: ...


class DocumentsContract(Protocol):
    def create_document(
        self,
        *,
        context: IntegrationContext,
        document_type: str,
        title: str,
        content: str,
    ) -> str: ...


class StorageContract(Protocol):
    def put_audio_reference(
        self, *, context: IntegrationContext, object_key: str, metadata: dict[str, Any]
    ) -> str: ...


class AppointmentContract(Protocol):
    def validate_appointment(
        self, *, organization_id: str, appointment_id: str, patient_id: str
    ) -> dict[str, Any]: ...


class EncounterContract(Protocol):
    def validate_encounter(
        self, *, organization_id: str, encounter_id: str, patient_id: str
    ) -> dict[str, Any]: ...
