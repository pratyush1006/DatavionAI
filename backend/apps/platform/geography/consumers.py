"""Authenticated WebSocket consumer for Geography live tracking."""

from __future__ import annotations

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.platform.geography.models.tracking import TrackingParticipant
from apps.platform.geography.policies.tracking import validate_tracking_sample
from apps.platform.geography.services.tracking import TrackingService


class TrackingConsumer(AsyncJsonWebsocketConsumer):
    """Receive device watchPosition samples and broadcast persisted updates."""

    async def connect(self):
        self.session_id = str(self.scope["url_route"]["kwargs"]["session_id"])
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return
        role = await self._role(self.session_id, str(user.pk))
        if role is None:
            await self.close(code=4403)
            return
        self.role = role
        self.group = f"geography_tracking_{self.session_id.replace('-', '')}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
        await self.send_json(
            {
                "type": "tracking.connected",
                "session_id": self.session_id,
                "role": self.role,
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group"):
            await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get("type") == "tracking.ping":
            await self.send_json({"type": "tracking.pong"})
            return
        if content.get("type") != "location.update":
            await self.send_json(
                {"type": "tracking.error", "detail": "Unsupported message type."}
            )
            return
        if self.role not in (
            TrackingParticipant.Role.OWNER,
            TrackingParticipant.Role.UPDATER,
        ):
            await self.send_json(
                {"type": "tracking.error", "detail": "Viewer cannot publish locations."}
            )
            return
        try:
            validate_tracking_sample(
                accuracy_meters=content.get("accuracy_meters"),
                speed_mps=content.get("speed_mps"),
                heading_degrees=content.get("heading_degrees"),
            )
            update = await self._record(content)
        except Exception as exc:
            await self.send_json({"type": "tracking.error", "detail": str(exc)})
            return
        await self.channel_layer.group_send(
            self.group,
            {
                "type": "tracking.location",
                "payload": TrackingService.serialize_update(update),
            },
        )

    async def tracking_location(self, event):
        await self.send_json({"type": "location.updated", "data": event["payload"]})

    @database_sync_to_async
    def _role(self, session_id, user_id):
        p = TrackingParticipant.objects.filter(
            session_id=session_id, user_id=user_id, is_active=True
        ).first()
        return p.role if p else None

    @database_sync_to_async
    def _record(self, content):
        return TrackingService.record_location(
            session_id=self.session_id,
            user_id=self.scope["user"].pk,
            latitude=content["latitude"],
            longitude=content["longitude"],
            accuracy_meters=content.get("accuracy_meters"),
            altitude_meters=content.get("altitude_meters"),
            speed_mps=content.get("speed_mps"),
            heading_degrees=content.get("heading_degrees"),
            recorded_at=content.get("recorded_at"),
            source=content.get("source", "device"),
            metadata=content.get("metadata") or {},
        )


__all__ = ("TrackingConsumer",)
