"""Authenticated WebSocket endpoint receiving binary audio and emitting live transcript events."""

import hashlib
import json

from apps.transcription.constants.live import LiveSessionStatus
from apps.transcription.integrations.device_platform import authorize_device_capture
from apps.transcription.integrations.live_provider import get_streaming_provider
from apps.transcription.models import LiveTranscriptionSession, LiveTranscriptSegment
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone


class LiveTranscriptionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        protocols = self.scope.get("subprotocols", [])
        if len(protocols) != 2 or protocols[0] != "datavion.ticket":
            await self.close(code=4401)
            return
        self.owner_id = await self._consume_ticket(protocols[1])
        if self.owner_id is None:
            await self.close(code=4401)
            return
        session = await self._session(self.owner_id)
        if session is None:
            await self.close(code=4404)
            return
        try:
            if session.device_id:
                await self._device(
                    session.organization_id, session.device_id, session.patient_id
                )
            self.provider = get_streaming_provider()
            self.provider.start(
                session_id=str(session.session_id),
                language=session.language,
                mime_type=session.audio_mime_type,
            )
            await self.accept(subprotocol="datavion.ticket")
            await self._status(LiveSessionStatus.RECORDING)
            await self.send_json(
                {
                    "type": "session.ready",
                    "session_id": str(session.session_id),
                    "status": "recording",
                }
            )
        except Exception:
            await self.close(code=4403)

    async def disconnect(self, code):
        if getattr(self, "provider", None):
            try:
                self.provider.close()
            except Exception:
                pass
        if hasattr(self, "session_id"):
            try:
                await self._mark_reconnecting()
            except Exception:
                pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            try:
                message = json.loads(text_data)
            except json.JSONDecodeError:
                await self.send_json({"type": "error", "code": "invalid_message"})
                return
            if message.get("type") == "session.stop":
                await self._finish_session()
                return
            await self.send_json({"type": "error", "code": "unsupported_message"})
            return
        if bytes_data is None:
            await self.send_json({"type": "error", "code": "audio_binary_required"})
            return
        session = await self._session(self.owner_id)
        if session is None or session.status not in {
            LiveSessionStatus.RECORDING,
            LiveSessionStatus.PAUSED,
        }:
            await self.send_json({"type": "error", "code": "session_not_recording"})
            return
        sequence = int(session.sequence_number) + 1
        try:
            for item in self.provider.push_audio(
                audio=bytes(bytes_data), sequence=sequence
            ):
                await self._segment(item)
                await self.send_json(
                    {
                        "type": "transcript.segment",
                        "kind": item.kind,
                        "sequence": item.sequence,
                        "text": item.text,
                        "speaker": item.speaker_label,
                        "confidence": item.confidence,
                    }
                )
            await self._advance(sequence)
        except Exception as exc:
            await self._record_error(str(exc))
            await self.send_json(
                {"type": "error", "code": exc.__class__.__name__, "message": str(exc)}
            )

    async def _finish_session(self):
        try:
            for item in self.provider.finish() or []:
                await self._segment(item)
                await self.send_json(
                    {
                        "type": "transcript.segment",
                        "kind": item.kind,
                        "sequence": item.sequence,
                        "text": item.text,
                        "speaker": item.speaker_label,
                        "confidence": item.confidence,
                    }
                )
            await self._complete()
            await self.send_json({"type": "session.completed"})
        except Exception as exc:
            await self._record_error(str(exc))
            await self.send_json(
                {"type": "error", "code": exc.__class__.__name__, "message": str(exc)}
            )

    @database_sync_to_async
    def _complete(self):
        session = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=self.session_id,
        )
        session.status = LiveSessionStatus.COMPLETED
        session.ended_at = timezone.now()
        session.save(update_fields=("status", "ended_at", "updated_at"))

    @database_sync_to_async
    def _mark_reconnecting(self):
        session = LiveTranscriptionSession.objects.filter(
            session_id=self.session_id,
        ).first()
        if session and session.status not in {
            LiveSessionStatus.COMPLETED,
            LiveSessionStatus.FAILED,
            LiveSessionStatus.CANCELLED,
        }:
            session.status = LiveSessionStatus.RECONNECTING
            session.save(update_fields=("status", "updated_at"))

    @database_sync_to_async
    def _session(self, user_id):
        return LiveTranscriptionSession.objects.filter(
            session_id=self.session_id, created_by_id=user_id
        ).first()

    @database_sync_to_async
    def _consume_ticket(self, ticket):
        now = timezone.now()
        ticket_hash = hashlib.sha256(ticket.encode("utf-8")).hexdigest()
        session = LiveTranscriptionSession.objects.filter(
            session_id=self.session_id,
            websocket_ticket_hash=ticket_hash,
            websocket_ticket_expires_at__gt=now,
        ).first()
        if session is None:
            return None
        owner_id = session.created_by_id
        session.websocket_ticket_hash = ""
        session.websocket_ticket_expires_at = None
        session.save(
            update_fields=(
                "websocket_ticket_hash",
                "websocket_ticket_expires_at",
                "updated_at",
            )
        )
        return owner_id

    @database_sync_to_async
    def _device(self, organization_id, device_id, patient_id):
        return authorize_device_capture(
            organization_id=organization_id, device_id=device_id, patient_id=patient_id
        )

    @database_sync_to_async
    def _status(self, status):
        s = LiveTranscriptionSession.objects.get(session_id=self.session_id)
        s.status = status
        s.started_at = s.started_at or timezone.now()
        s.save(update_fields=("status", "started_at", "updated_at"))

    @database_sync_to_async
    def _advance(self, sequence):
        s = LiveTranscriptionSession.objects.select_for_update().get(
            session_id=self.session_id
        )
        s.sequence_number = sequence
        s.last_audio_at = timezone.now()
        s.save(update_fields=("sequence_number", "last_audio_at", "updated_at"))

    @database_sync_to_async
    def _record_error(self, message):
        s = LiveTranscriptionSession.objects.filter(session_id=self.session_id).first()
        if s:
            s.status = LiveSessionStatus.FAILED
            s.last_error = message[:5000]
            s.save(update_fields=("status", "last_error", "updated_at"))

    @database_sync_to_async
    def _segment(self, item):
        LiveTranscriptSegment.objects.update_or_create(
            session_id=self.session_id,
            sequence=item.sequence,
            defaults={
                "kind": item.kind,
                "text": item.text,
                "speaker_label": item.speaker_label,
                "start_ms": item.start_ms,
                "end_ms": item.end_ms,
                "confidence": item.confidence,
                "provider_segment_id": item.provider_segment_id,
                "is_current": True,
            },
        )
