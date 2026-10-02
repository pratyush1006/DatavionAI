"""Live session orchestration across Device, Telemedicine, Appointment and Encounter boundaries."""

from django.db import transaction

from apps.transcription.constants.live import LiveSessionStatus, LiveSource
from apps.transcription.integrations.appointments import validate_appointment_context
from apps.transcription.integrations.device_platform import authorize_device_capture
from apps.transcription.integrations.encounters import validate_encounter_context
from apps.transcription.integrations.telemedicine import validate_telemedicine_session
from apps.transcription.models import LiveTranscriptionSession


class LiveTranscriptionService:
    @staticmethod
    @transaction.atomic
    def create_session(
        *,
        organization,
        patient,
        created_by,
        encounter=None,
        device_id=None,
        telemedicine_session_id=None,
        appointment=None,
        source=LiveSource.BROWSER,
        audio_mime_type="audio/webm",
        language="en",
        provider="",
        metadata=None,
    ):
        validate_encounter_context(
            encounter=encounter, organization_id=organization.id, patient_id=patient.id
        )
        validate_appointment_context(
            appointment=appointment,
            organization_id=organization.id,
            patient_id=patient.id,
        )
        if telemedicine_session_id:
            validate_telemedicine_session(
                organization_id=organization.id,
                session_id=telemedicine_session_id,
                patient_id=patient.id,
            )
        if device_id:
            authorize_device_capture(
                organization_id=organization.id,
                device_id=device_id,
                patient_id=patient.id,
            )
        return LiveTranscriptionSession.objects.create(
            organization=organization,
            patient=patient,
            created_by=created_by,
            encounter=encounter,
            device_id=device_id,
            telemedicine_session_id=telemedicine_session_id,
            appointment_id=getattr(appointment, "id", None),
            source=source,
            audio_mime_type=audio_mime_type,
            language=language,
            provider=provider,
            metadata=metadata or {},
            status=LiveSessionStatus.READY,
        )
